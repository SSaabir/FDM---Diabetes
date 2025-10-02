/* eslint-disable react-refresh/only-export-components */
import React, { useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthContext from './AuthConstants';
import { authAPI } from '../services/api';
import { 
  storeAuthData, 
  getAuthData, 
  clearAuthData, 
  handleLoginSuccess,
  refreshAuthState,
  getUserType,
  isAdmin,
  isSuperAdmin,
  hasPermission,
  getUserInfo,
  getDisplayName,
  getRoleDisplayText,
  isTokenExpired
} from '../utils/auth';

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [userType, setUserType] = useState(null);
  const [userInfo, setUserInfo] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Check for stored authentication data on app startup
    const initializeAuth = async () => {
      setIsLoading(true);
      
      try {
        // Try to refresh authentication state
        const authData = await refreshAuthState(authAPI);
        
        if (authData) {
          setUser(authData.userInfo);
          setUserType(authData.userType);
          setUserInfo(authData.userInfo);
        } else {
          // No valid authentication
          setUser(null);
          setUserType(null);
          setUserInfo(null);
        }
      } catch (error) {
        console.error('Auth initialization error:', error);
        // Don't clear data immediately on network errors, only on auth errors
        if (error.response?.status === 401 || error.response?.status === 403) {
          clearAuthData();
          setUser(null);
          setUserType(null);
          setUserInfo(null);
        } else {
          // For network errors, try to use cached data
          const cachedData = getAuthData();
          if (cachedData && !isTokenExpired()) {
            setUser(cachedData.userInfo);
            setUserType(cachedData.userType);
            setUserInfo(cachedData.userInfo);
          } else {
            clearAuthData();
            setUser(null);
            setUserType(null);
            setUserInfo(null);
          }
        }
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const login = async (email, password) => {
    setIsLoading(true);
    try {
      const response = await authAPI.login(email, password);
      const loginData = response.data;
      
      // Handle the unified login response
      const authData = handleLoginSuccess(loginData, navigate);
      
      // Update state
      setUser(authData.userInfo);
      setUserType(authData.userType);
      setUserInfo(authData.userInfo);
      
      setIsLoading(false);
      return true;
    } catch (error) {
      setIsLoading(false);
      throw error; // Re-throw to let the component handle the error
    }
  };

  const signup = async (userData) => {
    setIsLoading(true);
    try {
      await authAPI.signup(userData);
      setIsLoading(false);
      return true;
    } catch (error) {
      setIsLoading(false);
      throw error;
    }
  };

  const logout = () => {
    // Clear all authentication data
    clearAuthData();
    
    // Reset state
    setUser(null);
    setUserType(null);
    setUserInfo(null);
    
    // Navigate to login
    navigate('/login');
  };

  const updateUser = (updatedUserData) => {
    // Update the user state with new data
    const newUserData = { ...user, ...updatedUserData };
    setUser(newUserData);
    setUserInfo(newUserData);
    
    // Update stored data as well
    const authData = getAuthData();
    if (authData) {
      const updatedAuthData = {
        ...authData,
        userInfo: newUserData
      };
      storeAuthData(updatedAuthData);
    }
  };

  // Helper functions for checking user permissions
  const checkPermission = (requiredRole) => {
    return hasPermission(requiredRole);
  };

  const value = {
    // User state
    user,
    userType,
    userInfo,
    isAuthenticated: !!user,
    
    // Authentication functions
    login,
    logout,
    signup,
    updateUser,
    isLoading,
    
    // User type checks
    isAdmin: isAdmin(),
    isSuperAdmin: isSuperAdmin(),
    
    // Permission checking
    hasPermission: checkPermission,
    
    // User display helpers
    displayName: getDisplayName(userInfo),
    roleDisplayText: getRoleDisplayText(userType, userInfo),
    
    // Utility functions
    getUserType: () => getUserType(),
    getUserInfo: () => getUserInfo(),
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
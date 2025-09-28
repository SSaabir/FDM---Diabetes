/* eslint-disable react-refresh/only-export-components */
import React, { useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthContext from './AuthConstants';
import { authAPI } from '../services/api';

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // Check for stored token on app startup
    const token = localStorage.getItem('diabetesPredict_token');
    if (token) {
      // Verify token by calling getCurrentUser
      authAPI.getCurrentUser()
        .then(userData => {
          setUser(userData);
        })
        .catch(() => {
          // Token invalid, remove it
          localStorage.removeItem('diabetesPredict_token');
        })
        .finally(() => {
          setIsLoading(false);
        });
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = async (email, password) => {
    setIsLoading(true);
    try {
      const response = await authAPI.login(email, password);
      // Store the token
      localStorage.setItem('diabetesPredict_token', response.data.access_token);
      // Get user data
      const userData = await authAPI.getCurrentUser();
      setUser(userData);
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
    setUser(null);
    localStorage.removeItem('diabetesPredict_token');
    navigate('/login');
  };

  const value = {
    user,
    isAuthenticated: !!user,
    login,
    logout,
    signup,
    isLoading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
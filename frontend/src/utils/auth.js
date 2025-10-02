/**
 * Authentication utility functions for unified login system
 * Handles both user and admin authentication states
 */

// Storage keys
const STORAGE_KEYS = {
  TOKEN: 'diabetesPredict_token',
  USER_TYPE: 'diabetesPredict_user_type',
  USER_INFO: 'diabetesPredict_user_info',
  USER: 'diabetesPredict_user', // Legacy key for backward compatibility
};

/**
 * Store authentication data after successful login
 */
export const storeAuthData = (loginResponse) => {
  const { access_token, user_type, user_info } = loginResponse;
  
  // Store token
  localStorage.setItem(STORAGE_KEYS.TOKEN, access_token);
  
  // Store user type (user or admin)
  localStorage.setItem(STORAGE_KEYS.USER_TYPE, user_type);
  
  // Store user info
  localStorage.setItem(STORAGE_KEYS.USER_INFO, JSON.stringify(user_info));
  
  // Store complete user object for backward compatibility
  localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify({
    ...user_info,
    user_type
  }));
  
  return {
    token: access_token,
    userType: user_type,
    userInfo: user_info
  };
};

/**
 * Get stored authentication data
 */
export const getAuthData = () => {
  const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
  const userType = localStorage.getItem(STORAGE_KEYS.USER_TYPE);
  const userInfoStr = localStorage.getItem(STORAGE_KEYS.USER_INFO);
  
  if (!token || !userType || !userInfoStr) {
    return null;
  }
  
  try {
    const userInfo = JSON.parse(userInfoStr);
    return {
      token,
      userType,
      userInfo,
      isAuthenticated: true
    };
  } catch (error) {
    console.error('Error parsing stored user info:', error);
    clearAuthData();
    return null;
  }
};

/**
 * Clear all authentication data
 */
export const clearAuthData = () => {
  Object.values(STORAGE_KEYS).forEach(key => {
    localStorage.removeItem(key);
  });
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = () => {
  const authData = getAuthData();
  return authData !== null;
};

/**
 * Get user type (user or admin)
 */
export const getUserType = () => {
  const authData = getAuthData();
  return authData?.userType || null;
};

/**
 * Check if current user is admin
 */
export const isAdmin = () => {
  return getUserType() === 'admin';
};

/**
 * Check if current user is superadmin
 */
export const isSuperAdmin = () => {
  const authData = getAuthData();
  // Check for both 'superadmin' role and admin user type
  return authData?.userType === 'admin' && 
         (authData?.userInfo?.role === 'superadmin' || 
          authData?.userInfo?.email === 'superadmin@diabetes-prediction.com');
};

/**
 * Get user info
 */
export const getUserInfo = () => {
  const authData = getAuthData();
  return authData?.userInfo || null;
};

/**
 * Get redirect path based on user type and role
 */
export const getRedirectPath = (userType, userInfo) => {
  if (userType === 'admin') {
    const role = userInfo?.role;
    if (role === 'superadmin') {
      return '/admin/dashboard?role=superadmin';
    } else {
      return '/admin/dashboard?role=admin';
    }
  } else if (userType === 'user') {
    return '/dashboard';
  }
  
  // Default fallback
  return '/';
};

/**
 * Handle login response and routing
 */
export const handleLoginSuccess = (loginResponse, navigate) => {
  // Store authentication data
  const authData = storeAuthData(loginResponse);
  
  // Get redirect path
  const redirectPath = getRedirectPath(authData.userType, authData.userInfo);
  
  // Navigate to appropriate dashboard
  navigate(redirectPath);
  
  return authData;
};

/**
 * Format user display name
 */
export const getDisplayName = (userInfo) => {
  if (!userInfo) return 'User';
  
  if (userInfo.full_name) {
    return userInfo.full_name;
  }
  
  if (userInfo.email) {
    return userInfo.email.split('@')[0];
  }
  
  return 'User';
};

/**
 * Get user role display text
 */
export const getRoleDisplayText = (userType, userInfo) => {
  if (userType === 'admin') {
    const role = userInfo?.role;
    if (role === 'superadmin') {
      return 'Super Administrator';
    } else if (role === 'admin') {
      return 'Administrator';
    }
    return 'Admin';
  } else if (userType === 'user') {
    return 'User';
  }
  
  return 'Unknown';
};

/**
 * Check if user has permission for a specific action
 */
export const hasPermission = (requiredRole) => {
  const authData = getAuthData();
  
  if (!authData) return false;
  
  const { userType, userInfo } = authData;
  
  switch (requiredRole) {
    case 'user':
      return userType === 'user' || userType === 'admin';
    case 'admin':
      return userType === 'admin';
    case 'superadmin':
      return userType === 'admin' && 
             (userInfo?.role === 'superadmin' || 
              userInfo?.email === 'superadmin@diabetes-prediction.com');
    default:
      return false;
  }
};

/**
 * Get authorization header for API requests
 */
export const getAuthHeader = () => {
  const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
  return token ? `Bearer ${token}` : null;
};

/**
 * Check if token is expired (basic check)
 */
export const isTokenExpired = () => {
  const token = localStorage.getItem(STORAGE_KEYS.TOKEN);
  if (!token) return true;
  
  try {
    // Simple JWT decode (header.payload.signature)
    const payload = JSON.parse(atob(token.split('.')[1]));
    const currentTime = Date.now() / 1000;
    
    return payload.exp < currentTime;
  } catch (error) {
    console.error('Error checking token expiration:', error);
    return true;
  }
};

/**
 * Refresh authentication state (call this on app startup)
 */
export const refreshAuthState = async (authAPI) => {
  const authData = getAuthData();
  
  if (!authData || isTokenExpired()) {
    clearAuthData();
    return null;
  }
  
  try {
    // Verify token is still valid by making a request
    if (authData.userType === 'admin') {
      const response = await authAPI.getCurrentAdmin();
      return { ...authData, userInfo: response.data };
    } else {
      const response = await authAPI.getCurrentUser();
      return { ...authData, userInfo: response.data };
    }
  } catch (error) {
    console.error('Token verification failed:', error);
    clearAuthData();
    return null;
  }
};
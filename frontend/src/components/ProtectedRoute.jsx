import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Loader2, Shield, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export const ProtectedRoute = ({ children, requiredRole = null, allowedRoles = [] }) => {
  const { isAuthenticated, isLoading, userType, userInfo, hasPermission, logout } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin text-primary mx-auto mb-4" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location, message: "Please log in to access this page" }} replace />;
  }

  // Check specific role requirement
  if (requiredRole && !hasPermission(requiredRole)) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <div className="mx-auto w-12 h-12 bg-destructive/10 rounded-full flex items-center justify-center mb-4">
              <Shield className="h-6 w-6 text-destructive" />
            </div>
            <CardTitle className="text-xl">Access Denied</CardTitle>
            <CardDescription>
              You don't have permission to access this page.
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center space-y-4">
            <div className="text-sm text-muted-foreground">
              <p>Required role: <span className="font-semibold">{requiredRole}</span></p>
              <p>Your role: <span className="font-semibold">{userType === 'admin' ? userInfo?.role : userType}</span></p>
            </div>
            <div className="flex flex-col gap-2">
              <Button 
                onClick={() => window.history.back()} 
                variant="outline"
                className="w-full"
              >
                Go Back
              </Button>
              <Button 
                onClick={logout}
                variant="ghost" 
                size="sm"
                className="w-full text-muted-foreground"
              >
                Logout
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Check allowed roles array
  if (allowedRoles.length > 0) {
    const hasAllowedRole = allowedRoles.some(role => hasPermission(role));
    if (!hasAllowedRole) {
      return (
        <div className="min-h-screen bg-background flex items-center justify-center p-4">
          <Card className="w-full max-w-md">
            <CardHeader className="text-center">
              <div className="mx-auto w-12 h-12 bg-destructive/10 rounded-full flex items-center justify-center mb-4">
                <AlertCircle className="h-6 w-6 text-destructive" />
              </div>
              <CardTitle className="text-xl">Access Restricted</CardTitle>
              <CardDescription>
                This page is restricted to specific user roles.
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center space-y-4">
              <div className="text-sm text-muted-foreground">
                <p>Allowed roles: <span className="font-semibold">{allowedRoles.join(', ')}</span></p>
                <p>Your role: <span className="font-semibold">{userType === 'admin' ? userInfo?.role : userType}</span></p>
              </div>
              <div className="flex flex-col gap-2">
                <Button 
                  onClick={() => window.history.back()} 
                  variant="outline"
                  className="w-full"
                >
                  Go Back
                </Button>
                <Button 
                  onClick={logout}
                  variant="ghost" 
                  size="sm"
                  className="w-full text-muted-foreground"
                >
                  Logout
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      );
    }
  }

  return <>{children}</>;
};

// Convenience components for specific role protection
export const AdminOnlyRoute = ({ children }) => (
  <ProtectedRoute requiredRole="admin">{children}</ProtectedRoute>
);

export const SuperAdminOnlyRoute = ({ children }) => (
  <ProtectedRoute requiredRole="superadmin">{children}</ProtectedRoute>
);

export const UserRoute = ({ children }) => (
  <ProtectedRoute allowedRoles={['user', 'admin']}>{children}</ProtectedRoute>
);
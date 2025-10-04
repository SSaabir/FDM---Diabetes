import { Button } from "./ui/button.jsx";
import { Badge } from "./ui/badge.jsx";
import { Avatar, AvatarFallback, AvatarImage } from "./ui/avatar.jsx";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu.jsx";
import { Stethoscope, Sparkles, User, LogOut, Settings, UserCircle, ChevronDown, Menu, X, Shield, BarChart3 } from "lucide-react";
import { Link } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { useState } from "react";

const Header = () => {
  const { isAuthenticated, logout, user, isAdmin, isSuperAdmin } = useAuth();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <header className="border-b bg-card/50 backdrop-blur supports-[backdrop-filter]:bg-card/50">
      <div className="container mx-auto px-4 py-4">
        <nav className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-3 cursor-pointer hover:opacity-80 transition-opacity">
            <Stethoscope className="h-8 w-8 text-primary animate-pulse" />
            <h1 className="text-2xl font-bold text-primary">DiabetesPredict</h1>
          </Link>
          
          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            <Link to="/prediction" className="cursor-pointer">
              <Button variant="ghost" className="text-foreground hover:text-primary cursor-pointer transition-colors">
                Risk Assessment
              </Button>
            </Link>
            <Link to="/chat" className="cursor-pointer">
              <Button variant="ghost" className="text-foreground hover:text-primary cursor-pointer transition-colors">
                Health Chat
              </Button>
            </Link>
            <Link to="/about" className="cursor-pointer">
              <Button variant="ghost" className="text-foreground hover:text-primary cursor-pointer transition-colors">
                About Us
              </Button>
            </Link>
            <Link to="/faq" className="cursor-pointer">
              <Button variant="ghost" className="text-foreground hover:text-primary cursor-pointer transition-colors">
                FAQ
              </Button>
            </Link>
            <Badge variant="outline" className="flex items-center space-x-1">
              <Sparkles className="h-3 w-3" />
              <span>AI-Powered</span>
            </Badge>
          </div>

          {/* Mobile menu button and user menu */}
          <div className="flex items-center space-x-2">
            {/* Mobile menu toggle */}
            <Button
              variant="ghost"
              size="sm"
              className="md:hidden"
              onClick={toggleMobileMenu}
            >
              {isMobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </Button>

            {/* User menu (shown on both mobile and desktop) */}
            {isAuthenticated ? (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="flex items-center space-x-2 h-auto p-2">
                    <Avatar className="h-8 w-8">
                      <AvatarImage src={user?.avatar} alt={user?.full_name || user?.name || user?.email} />
                      <AvatarFallback>
                        {(user?.full_name || user?.name || user?.email)?.charAt(0)?.toUpperCase() || 'U'}
                      </AvatarFallback>
                    </Avatar>
                    <div className="hidden sm:flex flex-col items-start">
                      <span className="text-sm font-medium">
                        {user?.full_name || user?.name || user?.email}
                      </span>
                      <span className="text-xs text-muted-foreground">
                        {user?.role || 'User'}
                      </span>
                    </div>
                    <ChevronDown className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-56">
                  <DropdownMenuItem asChild>
                    <Link to="/profile" className="flex items-center w-full">
                      <UserCircle className="h-4 w-4 mr-2" />
                      View Profile
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
                    <Link to="/profile/edit" className="flex items-center w-full">
                      <Settings className="h-4 w-4 mr-2" />
                      Edit Profile
                    </Link>
                  </DropdownMenuItem>
                  
                  {/* Admin Navigation - Only show for admin users */}
                  {(isAdmin || isSuperAdmin) && (
                    <>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem asChild>
                        <Link to="/admin/dashboard" className="flex items-center w-full">
                          <Shield className="h-4 w-4 mr-2" />
                          Admin Dashboard
                        </Link>
                      </DropdownMenuItem>
                      <DropdownMenuItem asChild>
                        <Link to="/dashboard" className="flex items-center w-full">
                          <BarChart3 className="h-4 w-4 mr-2" />
                          User Dashboard
                        </Link>
                      </DropdownMenuItem>
                    </>
                  )}
                  
                  <DropdownMenuSeparator />
                  <DropdownMenuItem 
                    onClick={logout}
                    className="text-red-600 focus:text-red-600 cursor-pointer"
                  >
                    <LogOut className="h-4 w-4 mr-2" />
                    Logout
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            ) : (
              <Link to="/login">
                <Button className="gradient-medical">
                  <User className="h-4 w-4 mr-2" />
                  Login
                </Button>
              </Link>
            )}
          </div>
        </nav>

        {/* Mobile Navigation Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden mt-4 pb-4 border-t pt-4">
            <div className="flex flex-col space-y-3">
              <Link 
                to="/prediction" 
                onClick={() => setIsMobileMenuOpen(false)}
                className="text-foreground hover:text-primary py-2 px-3 rounded-md hover:bg-muted transition-colors cursor-pointer"
              >
                🩺 Risk Assessment
              </Link>
              <Link 
                to="/chat" 
                onClick={() => setIsMobileMenuOpen(false)}
                className="text-foreground hover:text-primary py-2 px-3 rounded-md hover:bg-muted transition-colors cursor-pointer"
              >
                💬 Health Chat
              </Link>
              <Link 
                to="/about" 
                onClick={() => setIsMobileMenuOpen(false)}
                className="text-foreground hover:text-primary py-2 px-3 rounded-md hover:bg-muted transition-colors cursor-pointer"
              >
                ℹ️ About Us
              </Link>
              <Link 
                to="/faq" 
                onClick={() => setIsMobileMenuOpen(false)}
                className="text-foreground hover:text-primary py-2 px-3 rounded-md hover:bg-muted transition-colors cursor-pointer"
              >
                ❓ FAQ
              </Link>
              <Link 
                to="/contact" 
                onClick={() => setIsMobileMenuOpen(false)}
                className="text-foreground hover:text-primary py-2 px-3 rounded-md hover:bg-muted transition-colors cursor-pointer"
              >
                📞 Contact Us
              </Link>
              <Link 
                to="/terms" 
                onClick={() => setIsMobileMenuOpen(false)}
                className="text-foreground hover:text-primary py-2 px-3 rounded-md hover:bg-muted transition-colors cursor-pointer"
              >
                📄 Terms & Conditions
              </Link>
              <div className="pt-2 mt-2 border-t">
                <Badge variant="outline" className="flex items-center space-x-1 w-fit">
                  <Sparkles className="h-3 w-3" />
                  <span>AI-Powered</span>
                </Badge>
              </div>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
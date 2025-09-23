import { Button } from "./ui/button.jsx";
import { Badge } from "./ui/badge.jsx";
import { Stethoscope, Sparkles, User } from "lucide-react";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <header className="border-b bg-card/50 backdrop-blur supports-[backdrop-filter]:bg-card/50">
      <div className="container mx-auto px-4 py-4">
        <nav className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-3">
            <Stethoscope className="h-8 w-8 text-primary animate-pulse" />
            <h1 className="text-2xl font-bold text-primary">DiabetesPredict</h1>
          </Link>
          
          <div className="hidden md:flex items-center space-x-6">
            <Link to="/prediction">
              <Button variant="ghost" className="text-foreground hover:text-primary">
                Risk Assessment
              </Button>
            </Link>
            <Link to="/chat">
              <Button variant="ghost" className="text-foreground hover:text-primary">
                Health Chat
              </Button>
            </Link>
            <Badge variant="outline" className="flex items-center space-x-1">
              <Sparkles className="h-3 w-3" />
              <span>AI-Powered</span>
            </Badge>
          </div>

          <Button className="gradient-medical">
            <User className="h-4 w-4 mr-2" />
            Login
          </Button>
        </nav>
      </div>
    </header>
  );
};

export default Header;
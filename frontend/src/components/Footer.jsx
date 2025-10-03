import { Stethoscope, Heart, Shield, Mail } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "./ui/button.jsx";

const Footer = () => {
  return (
    <footer className="border-t bg-card/50 backdrop-blur supports-[backdrop-filter]:bg-card/50">
      <div className="container mx-auto px-4 py-12">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Stethoscope className="h-6 w-6 text-primary" />
              <span className="font-bold text-lg text-primary">DiabetesPredict</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Professional diabetes risk assessment and health consultation platform powered by AI technology.
            </p>
          </div>
          
          <div>
            <h3 className="font-semibold mb-4 text-foreground">Services</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/prediction" className="text-muted-foreground hover:text-primary transition-colors cursor-pointer">
                  Risk Assessment
                </Link>
              </li>
              <li>
                <Link to="/chat" className="text-muted-foreground hover:text-primary transition-colors cursor-pointer">
                  AI Health Chat
                </Link>
              </li>
              <li className="text-muted-foreground">Health Monitoring</li>
              <li className="text-muted-foreground">Expert Consultation</li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold mb-4 text-foreground">Company</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/about" className="text-muted-foreground hover:text-primary transition-colors cursor-pointer">
                  About Us
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-muted-foreground hover:text-primary transition-colors cursor-pointer">
                  Contact Us
                </Link>
              </li>
              <li>
                <Link to="/faq" className="text-muted-foreground hover:text-primary transition-colors cursor-pointer">
                  FAQ
                </Link>
              </li>
              <li>
                <Link to="/terms" className="text-muted-foreground hover:text-primary transition-colors cursor-pointer">
                  Terms & Conditions
                </Link>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold mb-4 text-foreground">Support</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/faq" className="text-muted-foreground hover:text-primary transition-colors cursor-pointer">
                  Help Center
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-muted-foreground hover:text-primary transition-colors cursor-pointer">
                  Get Support
                </Link>
              </li>
              <li>
                <Link to="/terms" className="text-muted-foreground hover:text-primary transition-colors">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link to="/about" className="text-muted-foreground hover:text-primary transition-colors">
                  Our Mission
                </Link>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold mb-4 text-foreground">Connect</h3>
            <div className="space-y-3">
              <Button variant="outline" size="sm" className="w-full justify-start">
                <Mail className="h-4 w-4 mr-2" />
                Newsletter
              </Button>
              <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                <Heart className="h-4 w-4 text-red-500" />
                <span>Caring for your health</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                <Shield className="h-4 w-4 text-green-500" />
                <span>Privacy protected</span>
              </div>
            </div>
          </div>
        </div>
        
        <div className="border-t pt-8 text-center space-y-4">
          {/* Quick Links Row */}
          <div className="flex flex-wrap justify-center gap-6 mb-4">
            <Link to="/about" className="text-sm text-muted-foreground hover:text-primary transition-colors">
              About Us
            </Link>
            <Link to="/faq" className="text-sm text-muted-foreground hover:text-primary transition-colors">
              FAQ
            </Link>
            <Link to="/contact" className="text-sm text-muted-foreground hover:text-primary transition-colors">
              Contact
            </Link>
            <Link to="/terms" className="text-sm text-muted-foreground hover:text-primary transition-colors">
              Terms & Conditions
            </Link>
            <Link to="/prediction" className="text-sm text-muted-foreground hover:text-primary transition-colors">
              Risk Assessment
            </Link>
            <Link to="/chat" className="text-sm text-muted-foreground hover:text-primary transition-colors">
              Health Chat
            </Link>
          </div>
          
          <p className="text-sm text-muted-foreground">
            © 2024 DiabetesPredict. Professional diabetes risk assessment platform.
          </p>
          <p className="text-xs text-muted-foreground">
            ⚠️ This tool provides risk assessments and is not a substitute for professional medical advice
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
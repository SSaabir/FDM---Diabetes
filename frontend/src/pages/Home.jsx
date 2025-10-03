import { Button } from "../components/ui/button.jsx";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card.jsx";
import { Badge } from "../components/ui/badge.jsx";
import { 
  Stethoscope, 
  MessageCircle, 
  Calculator, 
  Heart, 
  Activity, 
  Shield, 
  TrendingUp,
  CheckCircle2,
  ArrowRight,
  Sparkles
} from "lucide-react";
import { Link } from "react-router-dom";
import Header from "../components/Header.jsx";
import Footer from "../components/Footer.jsx";
import { usePageTitle } from "../hooks/usePageTitle.js";

const Home = () => {
  usePageTitle("AI-Powered Diabetes Risk Assessment");

  return (
    <div className="min-h-screen bg-gradient-soft">
      
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="text-center max-w-4xl mx-auto">
          <h2 className="text-5xl font-bold text-primary mb-6 bounce-in">
            Your Health, Our Priority 🩺
          </h2>
          <p className="text-xl text-muted-foreground mb-8 slide-in">
            Get personalized diabetes risk assessments and expert health guidance 
            through our AI-powered platform. Take control of your health journey today! 💙
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            <Link to="/prediction">
              <Button size="lg" className="gradient-medical text-lg px-8 py-6">
                <Calculator className="h-5 w-5 mr-2" />
                Start Risk Assessment
                <ArrowRight className="h-5 w-5 ml-2" />
              </Button>
            </Link>
            <Link to="/chat">
              <Button variant="outline" size="lg" className="text-lg px-8 py-6">
                <MessageCircle className="h-5 w-5 mr-2" />
                Chat with Assistant
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h3 className="text-3xl font-bold text-primary mb-4">Why Choose DiabetesPredict? ✨</h3>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Comprehensive health assessment tools designed by medical professionals 
            to help you understand and manage your diabetes risk effectively.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          <Card className="medical-card text-center p-6">
            <div className="mb-4">
              <Calculator className="h-12 w-12 text-secondary mx-auto animate-float" />
            </div>
            <CardTitle className="text-lg mb-2">Smart Risk Assessment 🎯</CardTitle>
            <CardDescription>
              Advanced algorithms analyze multiple health factors to provide accurate diabetes risk predictions
            </CardDescription>
          </Card>

          <Card className="medical-card text-center p-6">
            <div className="mb-4">
              <MessageCircle className="h-12 w-12 text-accent mx-auto animate-bounce" />
            </div>
            <CardTitle className="text-lg mb-2">24/7 Health Assistant 🤖</CardTitle>
            <CardDescription>
              Get instant answers to your diabetes-related questions from our AI-powered chat assistant
            </CardDescription>
          </Card>

          <Card className="medical-card text-center p-6">
            <div className="mb-4">
              <Heart className="h-12 w-12 text-primary mx-auto animate-heartbeat" />
            </div>
            <CardTitle className="text-lg mb-2">Personalized Recommendations 💡</CardTitle>
            <CardDescription>
              Receive tailored health advice and actionable steps based on your unique risk profile
            </CardDescription>
          </Card>

          <Card className="medical-card text-center p-6">
            <div className="mb-4">
              <Shield className="h-12 w-12 text-secondary mx-auto pulse-gentle" />
            </div>
            <CardTitle className="text-lg mb-2">Privacy Protected 🔒</CardTitle>
            <CardDescription>
              Your health data is processed securely with complete privacy protection and confidentiality
            </CardDescription>
          </Card>

          <Card className="medical-card text-center p-6">
            <div className="mb-4">
              <Activity className="h-12 w-12 text-accent mx-auto animate-float" />
            </div>
            <CardTitle className="text-lg mb-2">Evidence-Based 📊</CardTitle>
            <CardDescription>
              All assessments are based on validated medical research and clinical guidelines
            </CardDescription>
          </Card>

          <Card className="medical-card text-center p-6">
            <div className="mb-4">
              <TrendingUp className="h-12 w-12 text-primary mx-auto animate-bounce" />
            </div>
            <CardTitle className="text-lg mb-2">Progress Tracking 📈</CardTitle>
            <CardDescription>
              Monitor your health improvements and track risk reduction over time
            </CardDescription>
          </Card>
        </div>
      </section>

      {/* Quick Links Section */}
      <section className="container mx-auto px-4 py-12">
        <div className="text-center mb-8">
          <h3 className="text-2xl font-bold text-primary mb-4">Explore More 🔍</h3>
          <p className="text-muted-foreground">
            Learn more about our platform and get the support you need
          </p>
        </div>
        
        <div className="grid md:grid-cols-4 gap-4 max-w-4xl mx-auto">
          <Link to="/about" className="group">
            <Card className="medical-card text-center p-4 h-full hover:shadow-lg transition-all duration-300 group-hover:scale-105">
              <div className="text-3xl mb-2">ℹ️</div>
              <h4 className="font-semibold text-sm text-primary mb-1">About Us</h4>
              <p className="text-xs text-muted-foreground">Learn about our mission and team</p>
            </Card>
          </Link>
          
          <Link to="/faq" className="group">
            <Card className="medical-card text-center p-4 h-full hover:shadow-lg transition-all duration-300 group-hover:scale-105">
              <div className="text-3xl mb-2">❓</div>
              <h4 className="font-semibold text-sm text-primary mb-1">FAQ</h4>
              <p className="text-xs text-muted-foreground">Find answers to common questions</p>
            </Card>
          </Link>
          
          <Link to="/contact" className="group">
            <Card className="medical-card text-center p-4 h-full hover:shadow-lg transition-all duration-300 group-hover:scale-105">
              <div className="text-3xl mb-2">📞</div>
              <h4 className="font-semibold text-sm text-primary mb-1">Contact</h4>
              <p className="text-xs text-muted-foreground">Get in touch with our team</p>
            </Card>
          </Link>
          
          <Link to="/terms" className="group">
            <Card className="medical-card text-center p-4 h-full hover:shadow-lg transition-all duration-300 group-hover:scale-105">
              <div className="text-3xl mb-2">📄</div>
              <h4 className="font-semibold text-sm text-primary mb-1">Terms</h4>
              <p className="text-xs text-muted-foreground">Review our terms and policies</p>
            </Card>
          </Link>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-12">
        <Card className="medical-card gradient-medical text-primary-foreground">
          <CardContent className="p-8 text-center">
            <div className="max-w-2xl mx-auto">
              <h3 className="text-3xl font-bold mb-4">Ready to Take Control? 🚀</h3>
              <p className="text-lg mb-6 opacity-90">
                Join thousands of users who have already taken the first step towards better health management. 
                Your wellness journey starts with understanding your risk!
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link to="/prediction">
                  <Button size="lg" variant="secondary" className="text-lg px-8 py-6">
                    <Calculator className="h-5 w-5 mr-2" />
                    Get My Risk Score
                  </Button>
                </Link>
                <Link to="/chat">
                  <Button size="lg" variant="outline" className="border-primary-foreground text-primary-foreground hover:bg-primary-foreground hover:text-primary text-lg px-8 py-6">
                    <MessageCircle className="h-5 w-5 mr-2" />
                    Ask Questions First
                  </Button>
                </Link>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Stats Section */}
      <section className="container mx-auto px-4 py-12">
        <div className="grid md:grid-cols-4 gap-6">
          {[
            { number: "10K+", label: "Users Assessed", icon: CheckCircle2 },
            { number: "95%", label: "Accuracy Rate", icon: TrendingUp },
            { number: "24/7", label: "Support Available", icon: MessageCircle },
            { number: "100%", label: "Privacy Protected", icon: Shield }
          ].map((stat, index) => (
            <Card key={index} className="medical-card text-center p-6">
              <stat.icon className="h-8 w-8 text-accent mx-auto mb-3 animate-float" />
              <div className="text-2xl font-bold text-primary mb-1">{stat.number}</div>
              <div className="text-sm text-muted-foreground">{stat.label}</div>
            </Card>
          ))}
        </div>
      </section>
    </div>
  );
};

export default Home;

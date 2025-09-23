import React from 'react';
import { Link } from 'react-router-dom';
import { Layout } from '@/components/Layout';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { useAuth } from '@/contexts/AuthContext';
import { 
  Heart, 
  Activity, 
  MessageSquare, 
  FileText, 
  TrendingUp, 
  Shield, 
  Clock,
  ArrowRight
} from 'lucide-react';

export const Dashboard = () => {
  const { user } = useAuth();

  const features = [
    {
      icon: Activity,
      title: 'Risk Assessment',
      description: 'Complete a comprehensive health assessment to evaluate your diabetes risk',
      href: '/assessment',
      color: 'bg-primary-10 text-primary',
      buttonText: 'Start Assessment'
    },
    {
      icon: MessageSquare,
      title: 'Chat Assistant',
      description: 'Get instant answers about diabetes, health tips, and personalized recommendations',
      href: '/chat',
      color: 'bg-accent-10 text-accent',
      buttonText: 'Start Chatting'
    },
    {
      icon: FileText,
      title: 'FAQ & Resources',
      description: 'Browse frequently asked questions and comprehensive diabetes information',
      href: '/faq',
      color: 'bg-success-10 text-success',
      buttonText: 'Browse FAQ'
    },
    {
      icon: Shield,
      title: 'Admin Dashboard',
      description: 'Manage ML models, datasets, and monitor system performance',
      href: '/admin',
      color: 'bg-warning-10 text-warning',
      buttonText: 'Access Admin'
    }
  ];

  const benefits = [
    {
      icon: TrendingUp,
      title: 'Evidence-Based',
      description: 'Our assessment uses validated risk factors from medical research'
    },
    {
      icon: Shield,
      title: 'Privacy Protected',
      description: 'Your data is processed securely and not stored permanently'
    },
    {
      icon: Clock,
      title: 'Real-time Support',
      description: 'Get instant answers to your health questions 24/7'
    }
  ];

  return (
    <Layout>
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-foreground mb-6">
            Welcome back, {user?.name}!
          </h1>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto mb-8">
            Take control of your health with our comprehensive diabetes risk assessment 
            and AI-powered health assistant. Get personalized insights and recommendations 
            based on the latest medical research.
          </p>
          <div className="flex items-center justify-center space-x-2 mb-8">
            <Badge className="bg-success-10 text-success border-success-20">
              <Heart className="h-3 w-3 mr-1" />
              Trusted by Healthcare Professionals
            </Badge>
            <Badge className="bg-primary-10 text-primary border-primary-20">
              Evidence-Based Algorithm
            </Badge>
          </div>
        </div>

        {/* Main Features */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <Card key={feature.title} className="shadow-card card-hover border-0 bg-white">
                <CardHeader>
                  <div className={`w-12 h-12 rounded-xl ${feature.color} flex items-center justify-center mb-4 transition-all duration-300`}>
                    <Icon className="h-6 w-6" />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                  <CardDescription className="text-base">
                    {feature.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Button asChild className="w-full group button-bounce">
                    <Link to={feature.href}>
                      {feature.buttonText}
                      <ArrowRight className="ml-2 h-4 w-4 arrow-slide" />
                    </Link>
                  </Button>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Benefits Section */}
        <div className="bg-gradient-card rounded-2xl p-8 mb-16 shadow-card">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-foreground mb-4">
              Why Choose DiabetesPredict?
            </h2>
            <p className="text-lg text-muted-foreground">
              Professional-grade diabetes risk assessment at your fingertips
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {benefits.map((benefit) => {
              const Icon = benefit.icon;
              return (
                <div key={benefit.title} className="text-center group cursor-default">
                  <div className="w-16 h-16 bg-primary-10 text-primary rounded-2xl flex items-center justify-center mx-auto mb-4 transition-all duration-300 group-hover:scale-110 group-hover:bg-primary-20">
                    <Icon className="h-8 w-8" />
                  </div>
                  <h3 className="text-xl font-semibold text-foreground mb-2">
                    {benefit.title}
                  </h3>
                  <p className="text-muted-foreground">
                    {benefit.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-primary-5 rounded-2xl p-8 text-center">
          <h2 className="text-2xl font-bold text-foreground mb-4">
            Ready to assess your diabetes risk?
          </h2>
          <p className="text-lg text-muted-foreground mb-6">
            Take our comprehensive assessment and get personalized recommendations in minutes.
          </p>
          <Button size="lg" asChild className="shadow-medical">
            <Link to="/assessment">
              Start Risk Assessment
              <Activity className="ml-2 h-5 w-5" />
            </Link>
          </Button>
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;
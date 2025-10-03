import React, { useState } from 'react';
import { Layout } from '@/components/Layout';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { Badge } from '@/components/ui/badge';
import { Search, Heart, Shield, Activity, HelpCircle } from 'lucide-react';
import { usePageTitle } from "../hooks/usePageTitle.js";

const faqCategories = [
  {
    id: 'about-diabetes',
    title: 'About Diabetes',
    icon: Heart,
    color: 'bg-primary/10 text-primary',
    questions: [
      {
        id: 'what-is-diabetes',
        question: 'What is diabetes?',
        answer: 'Diabetes is a chronic health condition that affects how your body turns food into energy. When you have diabetes, your body either doesn\'t make enough insulin or can\'t use the insulin it makes effectively.'
      },
      {
        id: 'diabetes-types',
        question: 'What are the different types of diabetes?',
        answer: 'There are mainly three types: Type 1 diabetes (usually diagnosed in children and young adults), Type 2 diabetes (most common form, usually develops in adults), and Gestational diabetes (develops during pregnancy).'
      },
      {
        id: 'diabetes-symptoms',
        question: 'What are the common symptoms of diabetes?',
        answer: 'Common symptoms include increased thirst, frequent urination, unexplained weight loss, fatigue, blurred vision, slow-healing sores, and frequent infections.'
      }
    ]
  },
  {
    id: 'predictions',
    title: 'How Predictions Work',
    icon: Activity,
    color: 'bg-accent/10 text-accent',
    questions: [
      {
        id: 'prediction-accuracy',
        question: 'How accurate are the diabetes predictions?',
        answer: 'Our prediction model uses validated risk factors from medical research and has been trained on large datasets. However, predictions are estimates and should not replace professional medical advice. Always consult with healthcare providers for definitive diagnosis.'
      },
      {
        id: 'prediction-factors',
        question: 'What factors are used for predictions?',
        answer: 'We analyze multiple factors including age, BMI, family history, blood pressure, cholesterol levels, physical activity, smoking status, and other lifestyle factors that research has shown to be associated with diabetes risk.'
      },
      {
        id: 'prediction-frequency',
        question: 'How often should I check my diabetes risk?',
        answer: 'We recommend checking your risk every 6-12 months, or whenever you experience significant lifestyle changes (weight loss/gain, changes in physical activity, or other health conditions).'
      },
      {
        id: 'high-risk-action',
        question: 'What should I do if my risk assessment shows high risk?',
        answer: 'If you receive a high-risk assessment, schedule an appointment with your healthcare provider for proper testing and evaluation. Early detection and lifestyle modifications can significantly reduce your risk.'
      }
    ]
  },
  {
    id: 'privacy-security',
    title: 'Privacy & Security',
    icon: Shield,
    color: 'bg-success/10 text-success',
    questions: [
      {
        id: 'data-security',
        question: 'Is my health data secure?',
        answer: 'Yes, we take data security very seriously. All data is encrypted in transit and at rest. We comply with healthcare data protection standards and never share your personal health information with third parties without your consent.'
      },
      {
        id: 'data-storage',
        question: 'Where is my data stored?',
        answer: 'Your data is stored on secure, encrypted servers. We follow industry best practices for data protection and regularly audit our security measures.'
      },
      {
        id: 'data-sharing',
        question: 'Do you share my information with anyone?',
        answer: 'We do not share your personal health information with any third parties for commercial purposes. Any data sharing would only occur with your explicit consent and for legitimate medical or research purposes.'
      }
    ]
  },
  {
    id: 'using-app',
    title: 'Using the App',
    icon: HelpCircle,
    color: 'bg-warning/10 text-warning',
    questions: [
      {
        id: 'getting-started',
        question: 'How do I get started with the diabetes prediction?',
        answer: 'After logging in, navigate to the Risk Assessment page and fill out the comprehensive form with your health information. The system will analyze your data and provide a personalized risk assessment.'
      },
      {
        id: 'chat-assistant',
        question: 'How does the chat assistant work?',
        answer: 'Our AI-powered chat assistant can answer questions about diabetes, provide general health tips, and help you understand your risk assessment results. It\'s available 24/7 to provide support and information.'
      },
      {
        id: 'updating-info',
        question: 'Can I update my health information?',
        answer: 'Yes, you can update your health information at any time by going to the Risk Assessment page. Keeping your information current ensures more accurate predictions.'
      }
    ]
  }
];

export const FAQ = () => {
  usePageTitle("FAQ");
  const [searchTerm, setSearchTerm] = useState('');

  const filteredFAQs = faqCategories.map(category => ({
    ...category,
    questions: category.questions.filter(
      q => 
        q.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
        q.answer.toLowerCase().includes(searchTerm.toLowerCase())
    )
  })).filter(category => category.questions.length > 0);

  return (
    <Layout>
      <div className="max-w-4xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-foreground mb-4">
            Frequently Asked Questions
          </h1>
          <p className="text-xl text-muted-foreground mb-8">
            Find answers to common questions about diabetes prediction and our platform
          </p>
          
          {/* Search */}
          <div className="max-w-md mx-auto relative">
            <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
            <Input
              type="text"
              placeholder="Search questions..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        {/* FAQ Categories */}
        <div className="space-y-8">
          {filteredFAQs.map((category) => {
            const Icon = category.icon;
            return (
              <Card key={category.id} className="shadow-card">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-3">
                    <div className={`p-2 rounded-lg ${category.color}`}>
                      <Icon className="h-5 w-5" />
                    </div>
                    <span>{category.title}</span>
                    <Badge className="bg-slate-100 text-slate-700 border-slate-200">
                      {category.questions.length} questions
                    </Badge>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <Accordion type="single" collapsible className="w-full">
                    {category.questions.map((faq, index) => (
                      <AccordionItem key={faq.id} value={`item-${index}`}>
                        <AccordionTrigger className="text-left">
                          {faq.question}
                        </AccordionTrigger>
                        <AccordionContent className="text-muted-foreground">
                          {faq.answer}
                        </AccordionContent>
                      </AccordionItem>
                    ))}
                  </Accordion>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {filteredFAQs.length === 0 && searchTerm && (
          <div className="text-center py-12">
            <HelpCircle className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium text-foreground mb-2">
              No questions found
            </h3>
            <p className="text-muted-foreground">
              Try adjusting your search terms or browse our categories above.
            </p>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default FAQ;
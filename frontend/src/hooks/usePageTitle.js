import { useEffect } from 'react';

/**
 * Custom hook to set page title dynamically
 * @param {string} title - The page title to set
 * @param {string} suffix - Optional suffix (defaults to "DiabetesPredict")
 */
export const usePageTitle = (title, suffix = "DiabetesPredict") => {
  useEffect(() => {
    const fullTitle = title ? `${title} | ${suffix}` : suffix;
    document.title = fullTitle;
    
    // Update meta description based on page
    const metaDescription = document.querySelector('meta[name="description"]');
    if (metaDescription && title) {
      const pageDescriptions = {
        'Risk Assessment': 'Get your personalized diabetes risk assessment with our AI-powered prediction tool. Quick, accurate, and confidential health analysis.',
        'Health Chat': 'Chat with our AI health assistant for instant answers about diabetes management, symptoms, and prevention strategies.',
        'About Us': 'Learn about DiabetesPredict - our mission to provide accessible, AI-powered diabetes risk assessment and health guidance.',
        'FAQ': 'Find answers to frequently asked questions about diabetes risk assessment, our platform, and health recommendations.',
        'Contact Us': 'Get in touch with the DiabetesPredict team. We\'re here to help with your health assessment questions and support.',
        'Terms & Conditions': 'Review the terms and conditions for using DiabetesPredict platform and our health assessment services.',
        'Dashboard': 'View your health dashboard with diabetes risk assessments, recommendations, and health tracking insights.',
        'Profile': 'Manage your DiabetesPredict profile, health information, and account settings for personalized care.',
        'Login': 'Sign in to your DiabetesPredict account to access personalized health assessments and recommendations.',
        'Sign Up': 'Create your DiabetesPredict account to start your personalized diabetes risk assessment journey.'
      };
      
      const newDescription = pageDescriptions[title] || 'DiabetesPredict - AI-powered diabetes risk assessment platform. Get personalized health insights and expert guidance.';
      metaDescription.setAttribute('content', newDescription);
    }
    
    // Cleanup function to reset title when component unmounts
    return () => {
      document.title = suffix;
    };
  }, [title, suffix]);
};

export default usePageTitle;
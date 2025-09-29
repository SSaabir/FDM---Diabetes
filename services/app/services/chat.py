"""
Chat AI Service
Provides conversational diabetes guidance and health advice
"""
import logging
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class DiabetesChatService:
    """Service for AI-powered diabetes chat assistance"""
    
    def __init__(self):
        self.conversation_context = {}
        self.diabetes_knowledge_base = self._load_diabetes_knowledge()
        
    def _load_diabetes_knowledge(self) -> Dict[str, Any]:
        """Load diabetes knowledge base for chat responses"""
        return {
            "prevention": {
                "diet": [
                    "Focus on whole grains, fruits, and vegetables",
                    "Limit processed foods and added sugars",
                    "Control portion sizes",
                    "Choose lean proteins like fish, poultry, and legumes",
                    "Include healthy fats from nuts, seeds, and olive oil"
                ],
                "exercise": [
                    "Aim for 150 minutes of moderate aerobic activity per week",
                    "Include strength training exercises twice a week",
                    "Take regular walks after meals",
                    "Try activities you enjoy like dancing, swimming, or cycling",
                    "Start slowly and gradually increase intensity"
                ],
                "lifestyle": [
                    "Maintain a healthy weight",
                    "Get adequate sleep (7-9 hours per night)",
                    "Manage stress through relaxation techniques",
                    "Avoid smoking and limit alcohol consumption",
                    "Regular health checkups and screenings"
                ]
            },
            "symptoms": {
                "early_warning": [
                    "Increased thirst and urination",
                    "Unexplained weight loss",
                    "Fatigue and weakness",
                    "Blurred vision",
                    "Slow-healing wounds or frequent infections"
                ],
                "risk_factors": [
                    "Family history of diabetes",
                    "Being overweight or obese",
                    "Age 45 or older",
                    "Physical inactivity",
                    "High blood pressure or cholesterol"
                ]
            },
            "management": {
                "blood_sugar": [
                    "Monitor blood glucose regularly",
                    "Follow prescribed medication schedule",
                    "Keep a food and activity diary",
                    "Learn to count carbohydrates",
                    "Recognize signs of high and low blood sugar"
                ],
                "complications": [
                    "Regular eye exams to prevent diabetic retinopathy",
                    "Foot care to prevent diabetic neuropathy",
                    "Kidney function monitoring",
                    "Heart health management",
                    "Dental care and oral health"
                ]
            },
            "emergency": {
                "when_to_seek_help": [
                    "Blood sugar levels consistently above 300 mg/dL",
                    "Signs of diabetic ketoacidosis (fruity breath, nausea, vomiting)",
                    "Severe hypoglycemia (confusion, loss of consciousness)",
                    "Persistent symptoms that don't improve",
                    "Any concerning changes in health status"
                ]
            }
        }
    
    def generate_response(self, user_message: str, user_id: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate AI chat response for diabetes-related queries"""
        try:
            # Initialize user context if not exists
            if user_id not in self.conversation_context:
                self.conversation_context[user_id] = {
                    "messages": [],
                    "topics_discussed": [],
                    "preferences": {}
                }
            
            # Add user message to context
            self.conversation_context[user_id]["messages"].append({
                "type": "user",
                "message": user_message,
                "timestamp": datetime.now().isoformat()
            })
            
            # Analyze message intent
            intent = self._analyze_message_intent(user_message.lower())
            
            # Generate appropriate response
            response = self._generate_contextual_response(intent, user_message, user_id, context)
            
            # Add bot response to context
            self.conversation_context[user_id]["messages"].append({
                "type": "bot",
                "message": response["message"],
                "intent": intent,
                "timestamp": datetime.now().isoformat()
            })
            
            # Update discussed topics
            if intent not in self.conversation_context[user_id]["topics_discussed"]:
                self.conversation_context[user_id]["topics_discussed"].append(intent)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating chat response: {str(e)}")
            return {
                "message": "I'm sorry, I'm having trouble processing your request right now. Please try again or consult with a healthcare professional.",
                "intent": "error",
                "suggestions": ["Contact your healthcare provider", "Try rephrasing your question"],
                "source": "error_handler"
            }
    
    def _analyze_message_intent(self, message: str) -> str:
        """Analyze user message to determine intent"""
        
        # Define intent keywords
        intents = {
            "prevention": ["prevent", "avoid", "reduce risk", "healthy habits", "lifestyle"],
            "diet": ["food", "eat", "diet", "nutrition", "meal", "carbs", "sugar", "calories"],
            "exercise": ["exercise", "workout", "physical activity", "gym", "walking", "fitness"],
            "symptoms": ["symptoms", "signs", "feel", "experiencing", "warning"],
            "blood_sugar": ["blood sugar", "glucose", "a1c", "monitoring", "levels"],
            "medication": ["medication", "insulin", "pills", "treatment", "prescription"],
            "complications": ["complications", "eyes", "feet", "kidney", "heart", "neuropathy"],
            "emergency": ["emergency", "urgent", "severe", "dangerous", "hospital"],
            "general_info": ["what is", "explain", "tell me about", "information", "learn"],
            "support": ["help", "support", "advice", "guidance", "recommend"]
        }
        
        # Check for emergency keywords first
        emergency_keywords = ["emergency", "urgent", "severe", "chest pain", "unconscious", "911"]
        if any(keyword in message for keyword in emergency_keywords):
            return "emergency"
        
        # Find best matching intent
        best_intent = "general_info"
        max_matches = 0
        
        for intent, keywords in intents.items():
            matches = sum(1 for keyword in keywords if keyword in message)
            if matches > max_matches:
                max_matches = matches
                best_intent = intent
        
        return best_intent
    
    def _generate_contextual_response(self, intent: str, message: str, user_id: str, context: Optional[Dict]) -> Dict[str, Any]:
        """Generate contextual response based on intent and user context"""
        
        if intent == "emergency":
            return {
                "message": "🚨 If you're experiencing a medical emergency, please call 911 or go to the nearest emergency room immediately. For diabetes emergencies, look for signs of diabetic ketoacidosis or severe hypoglycemia.",
                "intent": intent,
                "suggestions": ["Call 911", "Go to emergency room", "Contact your doctor immediately"],
                "urgency": "high",
                "source": "emergency_protocol"
            }
        
        elif intent == "prevention":
            prevention_tips = self.diabetes_knowledge_base["prevention"]
            return {
                "message": "🛡️ Great question about diabetes prevention! Here are key strategies:\n\n" +
                          "**Diet**: " + ", ".join(prevention_tips["diet"][:3]) + "\n\n" +
                          "**Exercise**: " + ", ".join(prevention_tips["exercise"][:2]) + "\n\n" +
                          "**Lifestyle**: " + ", ".join(prevention_tips["lifestyle"][:3]),
                "intent": intent,
                "suggestions": ["Tell me about healthy foods", "Show me exercise plans", "Lifestyle tips"],
                "source": "prevention_guide"
            }
        
        elif intent == "diet":
            diet_advice = self.diabetes_knowledge_base["prevention"]["diet"]
            return {
                "message": "🍎 Nutrition is crucial for diabetes prevention and management! Here's what I recommend:\n\n" +
                          "• " + "\n• ".join(diet_advice) + "\n\n" +
                          "Would you like specific meal ideas or help with carbohydrate counting?",
                "intent": intent,
                "suggestions": ["Meal planning ideas", "Carb counting help", "Healthy recipes"],
                "source": "nutrition_guide"
            }
        
        elif intent == "exercise":
            exercise_tips = self.diabetes_knowledge_base["prevention"]["exercise"]
            return {
                "message": "🏃‍♀️ Exercise is one of the best ways to prevent and manage diabetes! Here's a good starting plan:\n\n" +
                          "• " + "\n• ".join(exercise_tips) + "\n\n" +
                          "Remember to check with your healthcare provider before starting any new exercise program.",
                "intent": intent,
                "suggestions": ["Beginner workout plans", "Exercise safety tips", "Activity tracking"],
                "source": "fitness_guide"
            }
        
        elif intent == "symptoms":
            symptoms = self.diabetes_knowledge_base["symptoms"]["early_warning"]
            return {
                "message": "⚠️ Here are common early warning signs of diabetes:\n\n" +
                          "• " + "\n• ".join(symptoms) + "\n\n" +
                          "If you're experiencing any of these symptoms, especially multiple ones, please consult with a healthcare professional for proper evaluation.",
                "intent": intent,
                "suggestions": ["When to see a doctor", "Risk assessment", "Testing recommendations"],
                "source": "symptom_guide"
            }
        
        elif intent == "blood_sugar":
            bs_management = self.diabetes_knowledge_base["management"]["blood_sugar"]
            return {
                "message": "📊 Blood sugar management is key to diabetes care:\n\n" +
                          "• " + "\n• ".join(bs_management) + "\n\n" +
                          "Target ranges vary by individual, so work with your healthcare team to establish your personal goals.",
                "intent": intent,
                "suggestions": ["Blood sugar targets", "Monitoring tips", "Managing high/low levels"],
                "source": "glucose_management"
            }
        
        elif intent == "complications":
            complications_info = self.diabetes_knowledge_base["management"]["complications"]
            return {
                "message": "🔍 Preventing diabetes complications requires proactive care:\n\n" +
                          "• " + "\n• ".join(complications_info) + "\n\n" +
                          "Regular checkups and good diabetes management can prevent most complications.",
                "intent": intent,
                "suggestions": ["Screening schedules", "Prevention strategies", "Warning signs"],
                "source": "complications_guide"
            }
        
        else:  # general_info or support
            return {
                "message": "👋 Hello! I'm here to help with diabetes-related questions and support. I can provide information about:\n\n" +
                          "• Prevention strategies and lifestyle tips\n" +
                          "• Diet and nutrition guidance\n" +
                          "• Exercise recommendations\n" +
                          "• Symptom recognition\n" +
                          "• Blood sugar management\n" +
                          "• Complication prevention\n\n" +
                          "What would you like to know more about?",
                "intent": "general_info",
                "suggestions": ["Prevention tips", "Healthy eating", "Exercise plans", "Symptom checker"],
                "source": "general_assistance"
            }
    
    def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get conversation history for a user"""
        if user_id not in self.conversation_context:
            return []
        
        messages = self.conversation_context[user_id]["messages"]
        return messages[-limit:] if limit > 0 else messages
    
    def clear_conversation(self, user_id: str) -> bool:
        """Clear conversation history for a user"""
        try:
            if user_id in self.conversation_context:
                self.conversation_context[user_id] = {
                    "messages": [],
                    "topics_discussed": [],
                    "preferences": {}
                }
            return True
        except Exception:
            return False
    
    def get_suggested_questions(self, user_id: str) -> List[str]:
        """Get suggested questions based on conversation context"""
        base_suggestions = [
            "How can I prevent diabetes?",
            "What foods should I eat?",
            "What are the warning signs of diabetes?",
            "How much exercise do I need?",
            "How do I monitor my blood sugar?"
        ]
        
        if user_id not in self.conversation_context:
            return base_suggestions
        
        discussed_topics = self.conversation_context[user_id]["topics_discussed"]
        
        # Provide follow-up suggestions based on discussed topics
        follow_up_suggestions = {
            "diet": ["Can you suggest healthy meal plans?", "How do I count carbohydrates?"],
            "exercise": ["What exercises are safe for beginners?", "How do I start a fitness routine?"],
            "symptoms": ["When should I see a doctor?", "How do I get tested for diabetes?"],
            "prevention": ["What lifestyle changes are most important?", "How do I maintain motivation?"]
        }
        
        suggestions = base_suggestions.copy()
        for topic in discussed_topics:
            if topic in follow_up_suggestions:
                suggestions.extend(follow_up_suggestions[topic])
        
        return suggestions[:8]  # Limit to 8 suggestions

# Global chat service instance
chat_service = DiabetesChatService()
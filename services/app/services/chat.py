"""
Chat AI Service with Groq/Meta Llama Integration
Provides conversational diabetes guidance and health advice
"""
import logging
from typing import List, Dict, Any, Optional
import json
from datetime import datetime
from groq import Groq
from ..config import settings

logger = logging.getLogger(__name__)

class DiabetesChatService:
    """Service for AI-powered diabetes chat assistance using Groq/Meta Llama"""
    
    def __init__(self):
        self.conversation_context = {}
        self.groq_api_key = settings.groq_api_key
        self.groq_model = settings.groq_model
        
        # Debug settings
        logger.info(f"🔑 API Key present: {bool(self.groq_api_key)}")
        logger.info(f"🤖 Model: {self.groq_model}")
        
        # Initialize Groq client
        self.groq_client = None
        if self.groq_api_key:
            try:
                self.groq_client = Groq(api_key=self.groq_api_key)
                logger.info("✅ Groq client initialized successfully")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Groq client: {e}")
        else:
            logger.warning("⚠️ No Groq API key provided - chat will use fallback responses")
        
        # System prompt to restrict AI to diabetes and health information only
        self.system_prompt = """You are a specialized diabetes health information assistant powered by Meta Llama. 

IMPORTANT RESTRICTIONS:
- You can ONLY provide information about diabetes, blood sugar, diet, exercise, and general health topics
- You are NOT a doctor and cannot provide medical diagnosis or specific medical advice
- You must ALWAYS remind users to consult with healthcare professionals for medical decisions
- If asked about non-diabetes/non-health topics, politely redirect to diabetes-related information
- If asked for medical diagnosis, clearly state you cannot diagnose and recommend seeing a doctor

RESPONSE GUIDELINES:
- Be helpful, informative, and supportive
- Use simple, clear language
- Include relevant emojis to make responses friendly
- Always include a disclaimer about consulting healthcare professionals
- Provide practical, actionable advice when appropriate
- Stay focused on diabetes prevention, management, and general health

DISCLAIMER TO INCLUDE:
"⚠️ This information is for educational purposes only. I'm an AI assistant, not a medical professional. Always consult with your doctor or healthcare provider for personalized medical advice, diagnosis, or treatment decisions."
"""
    
    def generate_response(self, user_message: str, user_id: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Generate AI chat response using Groq/Meta Llama for diabetes-related queries"""
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
            
            # Check if Groq API is available
            if not self.groq_api_key:
                return self._generate_fallback_response(user_message, user_id)
            
            # Generate response using Groq API
            response = self._call_groq_api(user_message, user_id)
            
            # Add bot response to context
            self.conversation_context[user_id]["messages"].append({
                "type": "bot",
                "message": response["message"],
                "timestamp": datetime.now().isoformat()
            })
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating chat response: {str(e)}")
            return self._generate_error_response()
    
    def _call_groq_api(self, user_message: str, user_id: str) -> Dict[str, Any]:
        """Call Groq API with Meta Llama model using official SDK"""
        try:
            if not self.groq_client:
                logger.warning("Groq client not available, using fallback")
                return self._generate_fallback_response(user_message, user_id)
            
            # Get recent conversation for context
            recent_messages = self.get_conversation_history(user_id, limit=6)
            
            # Build messages for API
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add recent conversation context
            for msg in recent_messages[-4:]:  # Last 4 messages for context
                role = "user" if msg["type"] == "user" else "assistant"
                messages.append({"role": role, "content": msg["message"]})
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Make API call using Groq SDK with error handling for model issues
            try:
                completion = self.groq_client.chat.completions.create(
                    model=self.groq_model,
                    messages=messages,
                    max_tokens=1000,
                    temperature=0.7,
                    top_p=0.9,
                    stream=False
                )
            except Exception as model_error:
                # If model is decommissioned, try alternative models
                logger.warning(f"Model {self.groq_model} failed: {model_error}")
                alternative_models = [
                    "llama-3.3-70b-versatile",      # Current primary model
                    "llama-3.1-8b-instant",         # Fast fallback
                    "qwen/qwen3-32b",               # Alternative provider
                    "meta-llama/llama-4-scout-17b-16e-instruct"  # Latest Meta model
                ]
                
                for alt_model in alternative_models:
                    try:
                        logger.info(f"Trying alternative model: {alt_model}")
                        completion = self.groq_client.chat.completions.create(
                            model=alt_model,
                            messages=messages,
                            max_tokens=1000,
                            temperature=0.7,
                            top_p=0.9,
                            stream=False
                        )
                        # Update the working model for future use
                        self.groq_model = alt_model
                        logger.info(f"✅ Successfully switched to model: {alt_model}")
                        break
                    except Exception as alt_error:
                        logger.warning(f"Alternative model {alt_model} also failed: {alt_error}")
                        continue
                else:
                    # If all models fail, raise the last error
                    raise model_error
            
            ai_message = completion.choices[0].message.content.strip()
            
            # Ensure disclaimer is included
            if "⚠️" not in ai_message and "disclaimer" not in ai_message.lower():
                ai_message += "\n\n⚠️ This information is for educational purposes only. I'm an AI assistant, not a medical professional. Always consult with your doctor or healthcare provider for personalized medical advice."
            
            return {
                "message": ai_message,
                "intent": self._analyze_message_intent(user_message),
                "source": "groq_llama",
                "suggestions": self._generate_suggestions(user_message),
                "model_used": self.groq_model
            }
                
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            return self._generate_fallback_response(user_message, user_id)
    
    def _generate_fallback_response(self, user_message: str, user_id: str) -> Dict[str, Any]:
        """Generate fallback response when Groq API is unavailable"""
        intent = self._analyze_message_intent(user_message.lower())
        
        responses = {
            "prevention": "🛡️ Diabetes prevention focuses on healthy lifestyle choices: maintain a balanced diet with whole foods, exercise regularly (150 minutes per week), maintain healthy weight, get adequate sleep, and manage stress. These steps can significantly reduce your risk of developing type 2 diabetes.",
            
            "diet": "🍎 For diabetes-friendly eating: choose whole grains over refined carbs, include plenty of vegetables, opt for lean proteins, limit added sugars and processed foods, control portion sizes, and stay hydrated. Consider working with a nutritionist for personalized meal planning.",
            
            "exercise": "🏃‍♀️ Regular physical activity helps control blood sugar and prevents diabetes. Aim for 150 minutes of moderate exercise weekly, include both cardio and strength training, start slowly if you're a beginner, and check blood sugar before/after exercise if you have diabetes.",
            
            "symptoms": "⚠️ Common diabetes warning signs include increased thirst and urination, unexplained weight loss, fatigue, blurred vision, and slow-healing wounds. If you experience these symptoms, please see a healthcare provider for proper evaluation and testing.",
            
            "emergency": "🚨 If you're experiencing a medical emergency, call 911 immediately. For diabetes emergencies, watch for severe high/low blood sugar symptoms, diabetic ketoacidosis signs, or loss of consciousness.",
        }
        
        message = responses.get(intent, 
            "👋 I'm here to help with diabetes-related questions! I can provide information about prevention, diet, exercise, symptoms, and management. What would you like to know about diabetes and health?")
        
        message += "\n\n⚠️ This information is for educational purposes only. I'm an AI assistant, not a medical professional. Always consult with your doctor or healthcare provider for personalized medical advice."
        
        return {
            "message": message,
            "intent": intent,
            "source": "fallback",
            "suggestions": self._generate_suggestions(user_message)
        }
    
    def _generate_error_response(self) -> Dict[str, Any]:
        """Generate error response"""
        return {
            "message": "I'm sorry, I'm having trouble processing your request right now. Please try again in a moment, or consult with a healthcare professional for immediate assistance.\n\n⚠️ For urgent medical concerns, please contact your doctor or call 911.",
            "intent": "error",
            "source": "error",
            "suggestions": ["Try again later", "Contact your healthcare provider", "Ask a simpler question"]
        }
    
    def _analyze_message_intent(self, message: str) -> str:
        """Analyze user message to determine intent"""
        intents = {
            "prevention": ["prevent", "avoid", "reduce risk", "healthy habits", "lifestyle"],
            "diet": ["food", "eat", "diet", "nutrition", "meal", "carbs", "sugar", "calories"],
            "exercise": ["exercise", "workout", "physical activity", "gym", "walking", "fitness"],
            "symptoms": ["symptoms", "signs", "feel", "experiencing", "warning"],
            "blood_sugar": ["blood sugar", "glucose", "a1c", "monitoring", "levels"],
            "emergency": ["emergency", "urgent", "severe", "dangerous", "hospital", "911"]
        }
        
        # Check for emergency first
        if any(keyword in message for keyword in intents["emergency"]):
            return "emergency"
        
        # Find best matching intent
        best_intent = "general"
        max_matches = 0
        
        for intent, keywords in intents.items():
            matches = sum(1 for keyword in keywords if keyword in message)
            if matches > max_matches:
                max_matches = matches
                best_intent = intent
        
        return best_intent
    
    def _generate_suggestions(self, user_message: str) -> List[str]:
        """Generate relevant follow-up suggestions"""
        base_suggestions = [
            "How can I prevent diabetes?",
            "What foods should I eat?",
            "What are diabetes warning signs?",
            "How much exercise do I need?",
            "How do I check my blood sugar?"
        ]
        
        if "diet" in user_message.lower() or "food" in user_message.lower():
            return ["Healthy meal ideas", "Carb counting tips", "Foods to avoid", "Portion control"]
        elif "exercise" in user_message.lower() or "workout" in user_message.lower():
            return ["Beginner exercises", "Exercise safety", "Best workouts for diabetes", "Activity tracking"]
        elif "symptom" in user_message.lower() or "sign" in user_message.lower():
            return ["When to see a doctor", "Early warning signs", "Risk factors", "Testing options"]
        else:
            return base_suggestions
    
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
        """Get suggested questions based on user context"""
        try:
            base_suggestions = [
                "How can I prevent diabetes? 🛡️",
                "What foods should I eat? 🥗", 
                "What are diabetes symptoms? 🩺",
                "Exercise recommendations 💪"
            ]
            
            # If user has conversation history, provide context-aware suggestions
            if user_id in self.conversation_context:
                recent_messages = self.conversation_context[user_id]["messages"][-3:]
                if recent_messages:
                    last_topic = ""
                    for msg in reversed(recent_messages):
                        if msg.get("type") == "user":
                            last_topic = msg.get("message", "").lower()
                            break
                    
                    if "diet" in last_topic or "food" in last_topic:
                        return [
                            "How many carbs should I eat daily? 🍞",
                            "Best snacks for diabetics 🥜",
                            "Reading nutrition labels 📊",
                            "Meal timing tips ⏰"
                        ]
                    elif "exercise" in last_topic or "workout" in last_topic:
                        return [
                            "How often should I exercise? 🏃‍♂️",
                            "Pre-workout blood sugar checks 📈",
                            "Post-exercise recovery tips 💤",
                            "Safe exercise intensity levels ❤️"
                        ]
                    elif "symptom" in last_topic or "sign" in last_topic:
                        return [
                            "When should I call my doctor? 📞",
                            "Blood sugar testing frequency 🩸",
                            "Managing high blood sugar 📈",
                            "Emergency warning signs ⚠️"
                        ]
            
            return base_suggestions
            
        except Exception as e:
            logger.error(f"Error generating suggestions: {e}")
            return [
                "How can I manage diabetes? 💡",
                "Tell me about healthy eating 🥗",
                "Exercise tips for diabetics 💪",
                "Understanding blood sugar 📊"
            ]

# Global chat service instance
chat_service = DiabetesChatService()
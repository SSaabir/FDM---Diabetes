import { useState, useRef, useEffect } from "react";
import { Button } from "../components/ui/button.jsx";
import { Input } from "../components/ui/input.jsx";
import { Card } from "../components/ui/card.jsx";
import { Send, MessageCircle, Heart, Activity, Stethoscope, User, Bot } from "lucide-react";
import { Link } from "react-router-dom";
import Header from "../components/Header.jsx";
import Footer from "../components/Footer.jsx";

const Chat = () => {
  const [messages, setMessages] = useState([
    {
      id: '1',
      text: "Hello! 👋 I'm your diabetes health assistant. How can I help you today? I can provide information about diabetes management, symptoms, or help you understand your health better! 🩺💙",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [newMessage, setNewMessage] = useState("");
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = () => {
    if (!newMessage.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      text: newMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setNewMessage("");

    // Simulate bot response
    setTimeout(() => {
      const botResponse = {
        id: (Date.now() + 1).toString(),
        text: getBotResponse(newMessage),
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botResponse]);
    }, 1000);
  };

  const getBotResponse = (message) => {
    const lowerMessage = message.toLowerCase();
    
    if (lowerMessage.includes('diabetes') || lowerMessage.includes('diabetic')) {
      return "Diabetes is a serious condition that affects how your body processes blood sugar. There are two main types: Type 1 and Type 2. Would you like me to explain the differences or discuss management strategies? 📊💡";
    } else if (lowerMessage.includes('symptom')) {
      return "Common diabetes symptoms include increased thirst, frequent urination, unexplained weight loss, fatigue, and blurred vision. If you're experiencing these symptoms, it's important to consult with a healthcare professional. 🩺⚡";
    } else if (lowerMessage.includes('diet') || lowerMessage.includes('food')) {
      return "A balanced diet is crucial for diabetes management! Focus on whole grains, lean proteins, healthy fats, and plenty of vegetables. Monitoring carbohydrate intake is also important. 🥗💚";
    } else if (lowerMessage.includes('exercise') || lowerMessage.includes('activity')) {
      return "Regular physical activity helps manage blood sugar levels! Aim for at least 150 minutes of moderate exercise per week. Always consult your doctor before starting a new exercise program. 🏃‍♀️💪";
    } else if (lowerMessage.includes('blood sugar') || lowerMessage.includes('glucose')) {
      return "Blood sugar monitoring is essential for diabetes management. Normal fasting glucose is typically 70-100 mg/dL. Your doctor can help you understand your target ranges. 📈🎯";
    } else {
      return "I'm here to help with diabetes-related questions! You can ask me about symptoms, diet, exercise, blood sugar management, or use our prediction tool to assess your risk. How can I assist you? 🤖💙";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-soft">
      {/* Chat Container */}
      <div className="container mx-auto px-4 py-6 max-w-4xl">
        <Card className="medical-card h-[calc(100vh-200px)] flex flex-col">
          {/* Chat Header */}
          <div className="p-4 border-b bg-gradient-medical text-primary-foreground rounded-t-lg">
            <div className="flex items-center space-x-3">
              <div className="relative">
                <Bot className="h-8 w-8 bounce-in" />
                <Heart className="h-3 w-3 text-accent absolute -top-1 -right-1 animate-heartbeat" />
              </div>
              <div>
                <h2 className="font-semibold">Health Assistant</h2>
                <p className="text-sm opacity-90">Always here to help with your diabetes questions 💙</p>
              </div>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} slide-in`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-3 ${
                    message.sender === 'user'
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-secondary/10 text-secondary-foreground border'
                  }`}
                >
                  <div className="flex items-start space-x-2">
                    {message.sender === 'bot' && (
                      <Bot className="h-4 w-4 text-secondary mt-0.5 flex-shrink-0" />
                    )}
                    {message.sender === 'user' && (
                      <User className="h-4 w-4 text-primary-foreground mt-0.5 flex-shrink-0" />
                    )}
                    <div>
                      <p className="text-sm">{message.text}</p>
                      <p className={`text-xs mt-1 ${
                        message.sender === 'user' ? 'text-primary-foreground/70' : 'text-muted-foreground'
                      }`}>
                        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Suggestions */}
          <div className="p-3 border-t bg-muted/30">
            <p className="text-xs text-muted-foreground mb-2">Quick questions:</p>
            <div className="flex flex-wrap gap-2">
              {[
                "What are diabetes symptoms? 🩺",
                "Diet recommendations 🥗",
                "Exercise tips 💪",
                "Blood sugar monitoring 📊"
              ].map((suggestion) => (
                <Button
                  key={suggestion}
                  variant="outline"
                  size="sm"
                  className="text-xs"
                  onClick={() => setNewMessage(suggestion)}
                >
                  {suggestion}
                </Button>
              ))}
            </div>
          </div>

          {/* Input */}
          <div className="p-4 border-t">
            <div className="flex space-x-2">
              <Input
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Ask me about diabetes management, symptoms, or health tips... 💬"
                className="flex-1"
              />
              <Button
                onClick={handleSendMessage}
                disabled={!newMessage.trim()}
                className="gradient-accent"
              >
                <Send className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </Card>

        {/* Info Cards */}
        <div className="grid md:grid-cols-3 gap-4 mt-6">
          <Card className="medical-card p-4 text-center">
            <Activity className="h-8 w-8 text-secondary mx-auto mb-2 animate-float" />
            <h3 className="font-semibold text-sm">Real-time Support</h3>
            <p className="text-xs text-muted-foreground">Get instant answers to your health questions</p>
          </Card>
          <Card className="medical-card p-4 text-center">
            <Heart className="h-8 w-8 text-accent mx-auto mb-2 animate-heartbeat" />
            <h3 className="font-semibold text-sm">Caring Assistance</h3>
            <p className="text-xs text-muted-foreground">Personalized support for your wellness journey</p>
          </Card>
          <Card className="medical-card p-4 text-center">
            <Stethoscope className="h-8 w-8 text-primary mx-auto mb-2 pulse-gentle" />
            <h3 className="font-semibold text-sm">Professional Guidance</h3>
            <p className="text-xs text-muted-foreground">Evidence-based information you can trust</p>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Chat;
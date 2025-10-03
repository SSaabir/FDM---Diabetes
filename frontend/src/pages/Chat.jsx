import { useState, useRef, useEffect } from "react";
import { Button } from "../components/ui/button.jsx";
import { Input } from "../components/ui/input.jsx";
import { Card } from "../components/ui/card.jsx";
import { Send, MessageCircle, Heart, Activity, Stethoscope, User, Bot, Loader2, AlertCircle } from "lucide-react";
import { Badge } from "../components/ui/badge.jsx";
import { useToast } from "../hooks/use-toast.jsx";
import { chatAPI, apiHelpers } from "../services/api.js";
import Header from "../components/Header.jsx";
import Footer from "../components/Footer.jsx";
import { usePageTitle } from "../hooks/usePageTitle.js";
import * as Yup from "yup"; // ✅ Yup for validation

const Chat = () => {
  usePageTitle("Health Chat");
  const { toast } = useToast();
  const [messages, setMessages] = useState([
    {
      id: "1",
      text: "Hello! 👋 I'm your diabetes health assistant. How can I help you today? I can provide information about diabetes management, symptoms, or help you understand your health better! 🩺💙",
      sender: "bot",
      timestamp: new Date(),
      intent: "greeting",
    },
  ]);
  const [newMessage, setNewMessage] = useState("");
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([
    "How can I prevent diabetes? 🛡️",
    "What foods should I eat? 🥗",
    "What are diabetes symptoms? 🩺",
    "Exercise recommendations 💪",
  ]);

  const messagesEndRef = useRef(null);

  // ✅ Yup schema for validation
  const messageSchema = Yup.object().shape({
    text: Yup.string()
      .trim()
      .required("Message cannot be empty")
      .max(300, "Message must be under 300 characters"),
  });

  // ✅ Load history + suggestions on mount
  useEffect(() => {
    loadChatHistory();
    loadSuggestions();
  }, []);

  const loadChatHistory = async () => {
    try {
      const response = await chatAPI.getHistory(10);
      const result = apiHelpers.handleSuccess(response);

      if (result.success && result.data.messages.length > 0) {
        const apiMessages = result.data.messages.map((msg, index) => ({
          id: `history_${index}`,
          text: msg.message,
          sender: msg.type === "user" ? "user" : "bot",
          timestamp: new Date(msg.timestamp),
          intent: msg.intent,
          urgency: msg.urgency,
        }));
        setMessages(apiMessages);
      }
    } catch (error) {
      console.warn("Failed to load chat history:", error);
      // Keep default greeting
    }
  };

  const loadSuggestions = async () => {
    try {
      const response = await chatAPI.getSuggestions();
      const result = apiHelpers.handleSuccess(response);

      if (result.success) {
        setSuggestions(result.data.suggestions.slice(0, 4));
      }
    } catch (error) {
      console.warn("Failed to load suggestions:", error);
      // Keep defaults
    }
  };

  // ✅ Main send handler with validation + error fallback
  const handleSendMessage = async () => {
    try {
      await messageSchema.validate({ text: newMessage }, { abortEarly: false });
      setErrors({});
    } catch (err) {
      const newErrors = {};
      if (err.inner) {
        err.inner.forEach((e) => {
          newErrors[e.path] = e.message;
        });
      }
      setErrors(newErrors);
      return;
    }

    if (!newMessage.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      text: newMessage,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    const messageText = newMessage;
    setNewMessage("");
    setIsLoading(true);

    try {
      const response = await chatAPI.sendMessage(messageText);
      const result = apiHelpers.handleSuccess(response);

      if (result.success) {
        const botMessage = {
          id: (Date.now() + 1).toString(),
          text: result.data.message,
          sender: "bot",
          timestamp: new Date(),
          intent: result.data.intent,
          urgency: result.data.urgency,
          suggestions: result.data.suggestions,
        };

        setMessages((prev) => [...prev, botMessage]);

        if (result.data.suggestions?.length > 0) {
          setSuggestions(result.data.suggestions.slice(0, 4));
        }

        if (result.data.urgency === "high") {
          toast({
            title: "⚠️ Important Health Notice",
            description: "The AI detected an urgent health concern. Please review carefully.",
            variant: "destructive",
          });
        }
      } else {
        throw new Error(result.message || "Chat failed");
      }
    } catch (error) {
      const errorResult = apiHelpers.handleError(error);

      // Fallback bot response
      const fallbackResponse = getBotResponseFallback(messageText);
      const botMessage = {
        id: (Date.now() + 1).toString(),
        text: fallbackResponse,
        sender: "bot",
        timestamp: new Date(),
        intent: "fallback",
      };

      setMessages((prev) => [...prev, botMessage]);

      toast({
        title: "Using Offline Mode",
        description: errorResult.message || "Connected to local assistant. For full AI features, check your connection.",
        variant: "default",
      });
    } finally {
      setIsLoading(false);
    }
  };

  // ✅ Fallback bot logic
  const getBotResponseFallback = (message) => {
    const lower = message.toLowerCase();

    if (lower.includes("diabetes")) {
      return "Diabetes affects how your body processes blood sugar. Would you like info on symptoms or management? 📊💡";
    } else if (lower.includes("symptom")) {
      return "Common diabetes symptoms: thirst, frequent urination, fatigue, blurred vision. Consult a doctor if concerned. 🩺⚡";
    } else if (lower.includes("diet") || lower.includes("food")) {
      return "Balanced diet is key! Focus on whole grains, lean proteins, healthy fats, and vegetables. 🥗💚";
    } else if (lower.includes("exercise") || lower.includes("activity")) {
      return "Exercise helps regulate blood sugar! Aim for 150 minutes/week of moderate activity. 🏃‍♀️💪";
    } else if (lower.includes("blood sugar") || lower.includes("glucose")) {
      return "Monitoring blood sugar is essential. Normal fasting: 70-100 mg/dL. Ask your doctor for personal targets. 📈🎯";
    }
    return "I can help with diabetes-related questions — diet, exercise, symptoms, or prediction tools. How can I assist you? 🤖💙";
  };

  return (
    <div className="min-h-screen bg-gradient-soft">
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
                <p className="text-sm opacity-90">
                  Always here to help with your diabetes questions 💙
                </p>
              </div>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 relative">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${
                  message.sender === "user" ? "justify-end" : "justify-start"
                } slide-in`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-3 ${
                    message.sender === "user"
                      ? "bg-primary text-primary-foreground"
                      : message.urgency === "high"
                      ? "bg-red-50 text-red-900 border border-red-200"
                      : "bg-secondary/10 text-secondary-foreground border"
                  }`}
                >
                  <div className="flex items-start space-x-2">
                    {message.sender === "bot" && (
                      <div
                        className={`h-4 w-4 mt-0.5 flex-shrink-0 ${
                          message.urgency === "high"
                            ? "text-red-600"
                            : "text-secondary"
                        }`}
                      >
                        {message.urgency === "high" ? (
                          <AlertCircle className="h-4 w-4" />
                        ) : (
                          <Bot className="h-4 w-4" />
                        )}
                      </div>
                    )}
                    {message.sender === "user" && (
                      <User className="h-4 w-4 text-primary-foreground mt-0.5 flex-shrink-0" />
                    )}
                    <div className="flex-1">
                      <p className="text-sm whitespace-pre-wrap">
                        {message.text}
                      </p>
                      {message.urgency === "high" && (
                        <Badge variant="destructive" className="mt-2 text-xs">
                          Urgent
                        </Badge>
                      )}
                      {message.intent && message.sender === "bot" && (
                        <p className="text-xs mt-1 opacity-70">
                          Topic: {message.intent.replace("_", " ")}
                        </p>
                      )}
                      <p
                        className={`text-xs mt-1 ${
                          message.sender === "user"
                            ? "text-primary-foreground/70"
                            : "text-muted-foreground"
                        }`}
                      >
                        {message.timestamp.toLocaleTimeString([], {
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {/* Loading indicator */}
            {isLoading && (
              <div className="flex justify-start slide-in">
                <div className="max-w-[80%] rounded-lg p-3 bg-secondary/10 text-secondary-foreground border">
                  <div className="flex items-start space-x-2">
                    <Loader2 className="h-4 w-4 text-secondary mt-0.5 flex-shrink-0 animate-spin" />
                    <div>
                      <p className="text-sm">AI is thinking...</p>
                      <p className="text-xs text-muted-foreground mt-1">
                        Analyzing your question
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Quick Suggestions */}
          <div className="p-3 border-t bg-muted/30">
            <p className="text-xs text-muted-foreground mb-2">Quick questions:</p>
            <div className="flex flex-wrap gap-2">
              {suggestions.map((s, i) => (
                <Button
                  key={i}
                  variant="outline"
                  size="sm"
                  className="text-xs"
                  onClick={() => setNewMessage(s)}
                  disabled={isLoading}
                >
                  {s}
                </Button>
              ))}
            </div>
          </div>

          {/* Input */}
          <div className="p-4 border-t">
            <div className="flex flex-col space-y-2">
              <div className="flex space-x-2">
                <Input
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                  placeholder="Ask me about diabetes management, symptoms, or health tips... 💬"
                  className={`flex-1 ${errors.text ? "border-destructive" : ""}`}
                />
                <Button
                  onClick={handleSendMessage}
                  disabled={!newMessage.trim()}
                  className="gradient-accent"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
              {errors.text && (
                <p className="text-sm text-destructive">{errors.text}</p>
              )}
            </div>
          </div>
        </Card>

        {/* Info Cards */}
        <div className="grid md:grid-cols-3 gap-4 mt-6">
          <Card className="medical-card p-4 text-center">
            <Activity className="h-8 w-8 text-secondary mx-auto mb-2 animate-float" />
            <h3 className="font-semibold text-sm">Real-time Support</h3>
            <p className="text-xs text-muted-foreground">
              Get instant answers to your health questions
            </p>
          </Card>
          <Card className="medical-card p-4 text-center">
            <Heart className="h-8 w-8 text-accent mx-auto mb-2 animate-heartbeat" />
            <h3 className="font-semibold text-sm">Caring Assistance</h3>
            <p className="text-xs text-muted-foreground">
              Personalized support for your wellness journey
            </p>
          </Card>
          <Card className="medical-card p-4 text-center">
            <Stethoscope className="h-8 w-8 text-primary mx-auto mb-2 pulse-gentle" />
            <h3 className="font-semibold text-sm">Professional Guidance</h3>
            <p className="text-xs text-muted-foreground">
              Evidence-based information you can trust
            </p>
          </Card>
        </div>
      </div>
    </div>
  );
};



export default Chat;

import React, { useState } from "react";
import * as Yup from "yup";

export default function ContactUs() {
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    subject: "",
    message: "",
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  // Yup schema
  const contactSchema = Yup.object().shape({
    firstName: Yup.string().required("Please enter your first name"),
    lastName: Yup.string().required("Please enter your last name"),
    email: Yup.string()
      .email("Please enter a valid email address")
      .required("Please enter your email"),
    subject: Yup.string().required("Please select a subject"),
    message: Yup.string().required("Please enter your message"),
  });

  const validateForm = async () => {
    try {
      await contactSchema.validate(formData, { abortEarly: false });
      setErrors({});
      return true;
    } catch (err) {
      const newErrors = {};
      err.inner.forEach((e) => {
        newErrors[e.path] = e.message;
      });
      setErrors(newErrors);
      return false;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!(await validateForm())) return;

    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setSuccess(true);
      setFormData({
        firstName: "",
        lastName: "",
        email: "",
        subject: "",
        message: "",
      });
      setTimeout(() => setSuccess(false), 5000);
    }, 2000);
  };

  return (
    <div className="max-w-5xl mx-auto p-6 bg-[#F3F3E0] text-[#183B4E] font-sans">
      {/* Grid */}
      <div className="grid md:grid-cols-2 gap-8 mb-8">
        {/* Form Section */}
        <div className="bg-white rounded-2xl p-10 shadow-xl border-2 border-[#27548A]/10 hover:-translate-y-1 hover:shadow-2xl transition">
          <h2 className="flex items-center gap-3 text-2xl font-bold text-[#27548A] mb-6">
            <div className="w-11 h-11 flex items-center justify-center rounded-xl bg-gradient-to-tr from-[#DDA853] to-[#e6b966]">
              📧
            </div>
            Send us a Message
          </h2>

          <form onSubmit={handleSubmit}>
            {/* Name Row */}
            <div className="grid md:grid-cols-2 gap-4">
              <div className="mb-5">
                <label className="block text-[#27548A] font-semibold mb-2">
                  First Name <span className="text-red-600">*</span>
                </label>
                <input
                  type="text"
                  value={formData.firstName}
                  onChange={(e) =>
                    setFormData({ ...formData, firstName: e.target.value })
                  }
                  className={`w-full p-4 rounded-lg border-2 ${
                    errors.firstName
                      ? "border-red-500 bg-red-50"
                      : "border-[#27548A]/20 bg-[#F3F3E0]"
                  } focus:outline-none focus:border-[#DDA853] focus:bg-white`}
                  placeholder="Your first name"
                />
                {errors.firstName && (
                  <p className="text-red-600 text-sm mt-1">{errors.firstName}</p>
                )}
              </div>
              <div className="mb-5">
                <label className="block text-[#27548A] font-semibold mb-2">
                  Last Name <span className="text-red-600">*</span>
                </label>
                <input
                  type="text"
                  value={formData.lastName}
                  onChange={(e) =>
                    setFormData({ ...formData, lastName: e.target.value })
                  }
                  className={`w-full p-4 rounded-lg border-2 ${
                    errors.lastName
                      ? "border-red-500 bg-red-50"
                      : "border-[#27548A]/20 bg-[#F3F3E0]"
                  } focus:outline-none focus:border-[#DDA853] focus:bg-white`}
                  placeholder="Your last name"
                />
                {errors.lastName && (
                  <p className="text-red-600 text-sm mt-1">{errors.lastName}</p>
                )}
              </div>
            </div>

            {/* Email */}
            <div className="mb-5">
              <label className="block text-[#27548A] font-semibold mb-2">
                Email Address <span className="text-red-600">*</span>
              </label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) =>
                  setFormData({ ...formData, email: e.target.value })
                }
                className={`w-full p-4 rounded-lg border-2 ${
                  errors.email
                    ? "border-red-500 bg-red-50"
                    : "border-[#27548A]/20 bg-[#F3F3E0]"
                } focus:outline-none focus:border-[#DDA853] focus:bg-white`}
                placeholder="your.email@example.com"
              />
              {errors.email && (
                <p className="text-red-600 text-sm mt-1">{errors.email}</p>
              )}
            </div>

            {/* Subject */}
            <div className="mb-5">
              <label className="block text-[#27548A] font-semibold mb-2">
                Subject <span className="text-red-600">*</span>
              </label>
              <select
                value={formData.subject}
                onChange={(e) =>
                  setFormData({ ...formData, subject: e.target.value })
                }
                className={`w-full p-4 rounded-lg border-2 ${
                  errors.subject
                    ? "border-red-500 bg-red-50"
                    : "border-[#27548A]/20 bg-[#F3F3E0]"
                } focus:outline-none focus:border-[#DDA853] focus:bg-white`}
              >
                <option value="">Select a topic</option>
                <option value="technical">Technical Support</option>
                <option value="billing">Billing Question</option>
                <option value="feature">Feature Request</option>
                <option value="bug">Bug Report</option>
                <option value="general">General Inquiry</option>
                <option value="partnership">Partnership</option>
              </select>
              {errors.subject && (
                <p className="text-red-600 text-sm mt-1">{errors.subject}</p>
              )}
            </div>

            {/* Message */}
            <div className="mb-5">
              <label className="block text-[#27548A] font-semibold mb-2">
                Message <span className="text-red-600">*</span>
              </label>
              <textarea
                value={formData.message}
                onChange={(e) =>
                  setFormData({ ...formData, message: e.target.value })
                }
                className={`w-full p-4 rounded-lg border-2 min-h-[120px] resize-y ${
                  errors.message
                    ? "border-red-500 bg-red-50"
                    : "border-[#27548A]/20 bg-[#F3F3E0]"
                } focus:outline-none focus:border-[#DDA853] focus:bg-white`}
                placeholder="Please describe your inquiry in detail..."
              />
              {errors.message && (
                <p className="text-red-600 text-sm mt-1">{errors.message}</p>
              )}
            </div>

            {/* Button */}
            <button
              type="submit"
              className="w-full py-4 bg-gradient-to-tr from-[#27548A] to-[#183B4E] text-white font-semibold text-lg rounded-lg shadow-md hover:-translate-y-1 hover:shadow-xl transition flex items-center justify-center"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></span>
                  Sending...
                </>
              ) : (
                "Send Message"
              )}
            </button>

            {success && (
              <div className="mt-5 p-4 bg-gradient-to-tr from-green-600 to-emerald-400 text-white rounded-lg font-semibold text-center">
                ✅ Thank you! Your message has been sent successfully. We'll get back to you within 24 hours.
              </div>
            )}
          </form>
        </div>

        {/* Info Section (unchanged) */}
        <div className="bg-gradient-to-tr from-[#27548A] to-[#183B4E] rounded-2xl p-10 text-white shadow-2xl">
          <h2 className="flex items-center gap-3 text-2xl font-bold mb-6">
            <div className="w-11 h-11 flex items-center justify-center rounded-xl bg-gradient-to-tr from-[#DDA853] to-[#e6b966]">
              📞
            </div>
            Get in Touch
          </h2>

          {[
            { icon: "📧", title: "Email Support", text: "support@clinicalapp.com" },
            { icon: "📱", title: "Phone Support", text: "+1 (555) 123-4567" },
            { icon: "⚡", title: "Emergency Support", text: "Critical issues: Call immediately" },
            {
              icon: "📍",
              title: "Office Address",
              text: "123 Medical Plaza, Suite 456\nHealthcare City, HC 12345",
            },
          ].map((item, idx) => (
            <div
              key={idx}
              className="flex items-center gap-4 mb-5 p-5 bg-white/10 rounded-xl hover:bg-white/20 hover:translate-x-1 transition"
            >
              <div className="w-12 h-12 flex items-center justify-center rounded-xl bg-[#DDA853] text-xl">
                {item.icon}
              </div>
              <div>
                <h4 className="text-lg font-semibold text-[#DDA853]">{item.title}</h4>
                <p className="opacity-90 whitespace-pre-line">{item.text}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Support Hours (unchanged) */}
      <div className="bg-white rounded-2xl p-8 shadow-xl border-2 border-[#DDA853]/20">
        <h3 className="flex items-center gap-2 text-[#27548A] text-xl font-bold mb-5">
          🕒 Support Hours
        </h3>
        <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4">
          <div className="bg-[#F3F3E0] p-4 rounded-lg border-l-4 border-[#DDA853] hover:-translate-y-1 transition">
            <strong className="text-[#27548A] block mb-1">Email Support</strong>
            <span>24/7 - We respond within 2 hours</span>
          </div>
          <div className="bg-[#F3F3E0] p-4 rounded-lg border-l-4 border-[#DDA853] hover:-translate-y-1 transition">
            <strong className="text-[#27548A] block mb-1">Phone Support</strong>
            <span>Mon-Fri: 8:00 AM - 8:00 PM EST</span>
          </div>
          <div className="bg-[#F3F3E0] p-4 rounded-lg border-l-4 border-[#DDA853] hover:-translate-y-1 transition">
            <strong className="text-[#27548A] block mb-1">Emergency Support</strong>
            <span>24/7 for critical issues</span>
          </div>
        </div>
      </div>
    </div>
  );
}

import { usePageTitle } from "../hooks/usePageTitle.js";

function AboutUs() {
  usePageTitle("About Us");
  
  return (
    <div className="relative flex flex-col min-h-screen bg-[#F3F3E0] p-8 gap-12">
      {/* Watermark */}
      <img
        src="/aboutus1.jpg"
        alt="Watermark"
        className="absolute top-0 left-0 w-full h-full object-cover opacity-7 pointer-events-none"
      />

      {/* Row 1: About Us + Core Values */}
      <div className="relative z-10 grid grid-cols-1 lg:grid-cols-2 gap-8 w-full">
        {/* About Us Box */}
        <div className="bg-white shadow-xl rounded-2xl p-10 text-left border-t-8 border-[#27548A] min-h-[350px] transform hover:scale-105 transition duration-300">
          <h1 className="text-3xl font-bold text-[#183B4E] mb-4">About Us 🩺 </h1>
          <p className="text-gray-700 leading-relaxed">
            We are dedicated to empowering individuals through early health insights. 
            Our platform uses advanced prediction models to analyze user-provided 
            health information and assess the risk of developing diabetes. 
            By delivering timely and reliable predictions, we help users take proactive steps 
            toward prevention, lifestyle improvement, and better health management.
          </p>

          {/* Impact Section */}
          <div className="grid grid-cols-3 gap-4 text-center mt-8">
            <div>
              <h2 className="text-2xl font-bold text-[#27548A]">24/7</h2>
              <p className="text-gray-600 text-sm">Health Assistant</p>
            </div>
            <div>
              <h2 className="text-2xl font-bold text-[#27548A]">10K+</h2>
              <p className="text-gray-600 text-sm">Health Predictions</p>
            </div>
            <div>
              <h2 className="text-2xl font-bold text-[#27548A]">100%</h2>
              <p className="text-gray-600 text-sm">Data Privacy</p>
            </div>
          </div>
        </div>

        {/* Core Values Section (no white wrapper) */}
        <div className="flex flex-col justify-start items-center w-full">
          <h2 className="text-3xl font-bold text-[#183B4E] mb-6 text-center">
            Why Choose Us?
          </h2>
          <div className="grid grid-cols-2 gap-6 w-full">
            {/* Value 1 */}
            <div className="bg-[#27548A] text-white rounded-xl shadow-lg p-6 transform hover:scale-105 transition duration-300">
              <h3 className="text-lg font-semibold mb-2">Innovation</h3>
              <p className="text-sm">
                Leveraging advanced technology to provide accurate diabetes risk predictions.
              </p>
            </div>
            {/* Value 2 */}
            <div className="bg-[#DDA853] text-white rounded-xl shadow-lg p-6 transform hover:scale-105 transition duration-300">
              <h3 className="text-lg font-semibold mb-2">Trust</h3>
              <p className="text-sm">Ensuring your health data is secure, private, and reliable.</p>
            </div>
            {/* Value 3 */}
            <div className="bg-[#183B4E] text-white rounded-xl shadow-lg p-6 transform hover:scale-105 transition duration-300">
              <h3 className="text-lg font-semibold mb-2">Accessibility</h3>
              <p className="text-sm">Available anytime, anywhere for everyone’s health insights.</p>
            </div>
            {/* Value 4 */}
            <div className="bg-[#27548A] text-white rounded-xl shadow-lg p-6 transform hover:scale-105 transition duration-300">
              <h3 className="text-lg font-semibold mb-2">Care</h3>
              <p className="text-sm">Supporting users with personalized guidance and preventive health tips.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Row 2: Mission + Vision */}
      <div className="relative z-10 grid grid-cols-1 lg:grid-cols-2 gap-8 w-full">
        {/* Mission Box */}
        <div className="bg-white shadow-xl rounded-2xl p-10 text-left border-t-8 border-[#DDA853] min-h-[300px] transform hover:scale-105 transition duration-300">
          <h1 className="text-3xl font-bold text-[#183B4E] mb-4">Our Mission 🎯 </h1>
          <p className="text-gray-700 leading-relaxed">
            To provide accessible, accurate, and user-friendly diabetes risk predictions
            that support healthier living. We strive to bridge the gap between
            technology and healthcare, giving people the tools they need to make 
            informed decisions and reduce the risk of chronic illness.
          </p>
        </div>

        {/* Vision Box */}
        <div className="bg-white shadow-xl rounded-2xl p-10 text-left border-t-8 border-[#27548A] min-h-[300px] transform hover:scale-105 transition duration-300">
          <h1 className="text-3xl font-bold text-[#183B4E] mb-4">Our Vision 🌍 </h1>
          <p className="text-gray-700 leading-relaxed">
            To become a leading global platform for digital diabetes prevention and awareness 
            empowering communities with innovative technology, data-driven insights,
             and a commitment to building healthier futures.
          </p>
        </div>
      </div>
    </div>
  );
}

export default AboutUs;

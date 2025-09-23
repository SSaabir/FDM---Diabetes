function Home() {
  return (
    <div className="min-h-screen bg-[#F3F3E0] flex flex-col">
      {/* Navigation Bar */}
      <nav className="bg-[#27548A] text-white py-4 shadow-md">
        <ul className="flex justify-end space-x-8 font-semibold pr-8 items-center">
          <li className="hover:text-[#DDA853] cursor-pointer">About Us</li>
          <li className="hover:text-[#DDA853] cursor-pointer">Contact Us</li>
          <li>
            <button className="bg-[#DDA853] text-[#183B4E] px-4 py-2 rounded-lg font-semibold shadow hover:opacity-90 transition">
              Logout
            </button>
          </li>
        </ul>
      </nav>

      {/* Main Content */}
      <div className="flex flex-1 flex-col items-center justify-center text-center p-8">
        <h1 className="text-5xl font-bold text-[#183B4E] mb-6">
          Welcome to Diabetes Risk Predictor
        </h1>
        <p className="text-lg text-gray-700 max-w-2xl leading-relaxed mb-10">
          Take charge of your health today! Our platform analyzes your health data 
          to provide insights into potential diabetes risks and guides you toward 
          healthier choices. Start your journey towards preventive care now.
        </p>

        {/* Prediction Button */}
        <button className="bg-[#27548A] text-white px-8 py-3 rounded-xl text-lg font-semibold shadow-lg hover:bg-[#183B4E] transition">
          Get Your Prediction
        </button>
      </div>
    </div>
  );
}

export default Home;

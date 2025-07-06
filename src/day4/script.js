// script.js

// Initialize date variable
let currentDate = new Date();

// Function to get current date
function getCurrentDate() {
  return currentDate.toISOString().split("T")[0];
}

// Function to generate welcome screen content
function generateWelcomeScreenContent() {
  const welcomeMessage = `Welcome to Code Companion! Today's Quote: "Believe you can and you're halfway there." - Theodore Roosevelt`;
  return `${welcomeMessage} Current Date: <span id="date">${getCurrentDate()}</span>`;
}

// Function to get user input
function getUserInput(event) {
  const userInput = document.getElementById("search-bar").value;
  return userInput;
}

// Function to generate idea using Ollama model
function generateIdea(userInput) {
  // (Implement Ollama's idea generation process here)
  // Return project idea as a string
  return "Project Idea: Implement a Python script to analyze weather data";
}

// Event listener for Generate Idea Button
document
  .getElementById("generate-idea-btn")
  .addEventListener("click", function () {
    const userInput = getUserInput();
    const output = generateIdea(userInput);
    document.querySelector(
      ".output-container"
    ).innerHTML = `<h2>Project Idea:</h2><p>${output}</p>`;
  });

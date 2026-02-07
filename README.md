<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ESP32-CAM Smart Home System - README</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Google Font -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

  <!-- Font Awesome -->
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet">

  <style>
    :root {
      --bg: #0f172a;
      --card: #111827;
      --text: #e5e7eb;
      --muted: #9ca3af;
      --accent: #38bdf8;
      --border: #1f2933;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family: 'Inter', sans-serif;
      background: linear-gradient(120deg, #020617, #0f172a);
      color: var(--text);
      line-height: 1.7;
    }

    .container {
      max-width: 1000px;
      margin: auto;
      padding: 40px 20px 80px;
    }

    .card {
      background: rgba(17, 24, 39, 0.75);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 32px;
      margin-bottom: 28px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }

    h1 {
      font-size: 2.4rem;
      margin-bottom: 10px;
    }

    h2 {
      margin-top: 0;
      color: var(--accent);
    }

    h3 {
      margin-top: 30px;
    }

    p {
      color: var(--text);
      margin: 10px 0;
    }

    ul {
      padding-left: 22px;
    }

    li {
      margin: 8px 0;
    }

    .subtitle {
      color: var(--muted);
      font-size: 1.1rem;
      margin-bottom: 25px;
    }

    .icon {
      color: var(--accent);
      margin-right: 8px;
    }

    .stack {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }

    .stack div {
      background: #020617;
      border-radius: 14px;
      padding: 18px;
      border: 1px solid var(--border);
    }

    .footer {
      text-align: center;
      margin-top: 40px;
      color: var(--muted);
      font-size: 0.9rem;
    }

    hr {
      border: none;
      height: 1px;
      background: var(--border);
      margin: 30px 0;
    }

    code {
      background: #020617;
      padding: 4px 8px;
      border-radius: 6px;
      font-size: 0.9rem;
      color: var(--accent);
    }
  </style>
</head>

<body>
  <div class="container">

    <div class="card">
      <h1>🏠 ESP32-CAM Based Smart Home System</h1>
      <div class="subtitle">Final IoT Project</div>

      <p>
        A modern <strong>Internet of Things</strong> smart home dashboard built on
        <strong>ESP32-CAM</strong> that enables users to control virtual devices and
        camera features using <strong>natural language commands (text, voice, and image)</strong>
        supported by artificial intelligence.
      </p>

      <p>
        This project is developed as a <strong>final project of the Internet of Things (IoT) course</strong>.
      </p>
    </div>

    <div class="card">
      <h2>📌 Project Overview</h2>

      <p>
        Traditional smart home systems rely on fixed buttons or predefined commands.
      </p>

      <p>
        This project introduces an <strong>AI-based smart home system</strong> capable of understanding
        <strong>natural language commands in Persian and English</strong> and executing them intelligently.
      </p>

      <ul>
        <li><i class="icon fa-solid fa-globe"></i>Web Dashboard</li>
        <li><i class="icon fa-solid fa-keyboard"></i>Text Commands</li>
        <li><i class="icon fa-solid fa-microphone"></i>Voice Commands</li>
        <li><i class="icon fa-solid fa-hand"></i>Visual / Gesture Commands</li>
        <li><i class="icon fa-brands fa-telegram"></i>Telegram Bot</li>
      </ul>
    </div>

    <div class="card">
      <h2>✨ Features</h2>

      <ul>
        <li>🌐 Web-based UI with modern and responsive dashboard</li>
        <li>🧠 AI command processing using LLM APIs</li>
        <li>💡 Control of 3 independent virtual lamps with animations</li>
        <li>📸 ESP32-CAM image capture and display</li>
        <li>🔦 Camera flash ON/OFF control with real-time feedback</li>
      </ul>

      <hr>

      <h3>⭐ Additional Features</h3>

      <ul>
        <li>🎙️ Voice command support (Speech-to-Text)</li>
        <li>✋ Gesture-based control using Vision AI</li>
        <li>🤖 Telegram Bot integration</li>
        <li>📷 Advanced camera settings</li>
        <li>🗄️ Database for command history and image metadata</li>
        <li>🖌️ Advanced UI/UX with Dark & Light Mode and animations</li>
      </ul>
    </div>

    <div class="card">
      <h2>🧱 System Architecture</h2>

      <p><strong>Client–Server Architecture:</strong></p>

      <p>
        User Interface → Python Server → AI Services → ESP32-CAM
      </p>

      <h3>Responsibilities</h3>

      <ul>
        <li><strong>ESP32-CAM:</strong> Camera capture, flash control, Wi-Fi (Station + AP)</li>
        <li><strong>Python Server:</strong> API handling, AI processing, device states, database</li>
      </ul>
    </div>

    <div class="card">
      <h2>🛠️ Technology Stack</h2>

      <div class="stack">
        <div>
          <strong>Hardware</strong>
          <p>ESP32-CAM</p>
        </div>
        <div>
          <strong>Backend</strong>
          <p>Python (Django / FastAPI)<br>REST APIs<br>Production Server</p>
        </div>
        <div>
          <strong>Frontend</strong>
          <p>HTML, CSS, JavaScript<br>Responsive UI<br>Animations</p>
        </div>
        <div>
          <strong>AI & Database</strong>
          <p>LLM<br>Speech-to-Text<br>Vision AI<br>Database Storage</p>
        </div>
      </div>
    </div>

    <div class="card">
      <h2>🌍 Deployment</h2>

      <ul>
        <li>✅ Fully deployed on a real online server</li>
        <li>✅ Not a local-only implementation</li>
        <li>✅ Accessible via web browser</li>
        <li>✅ Suitable for real-world demonstration</li>
      </ul>
    </div>

    <div class="card">
      <h2>🎯 Educational Value & Conclusion</h2>

      <p>
        This project demonstrates practical IoT system design, AI integration in embedded systems,
        real-world client–server architecture, modern UI/UX design, and cloud deployment experience.
      </p>

      <p>
        It is a complete, production-level <strong>IoT Smart Home System</strong> designed to be
        scalable, modern, and user-friendly.
      </p>
    </div>

    <div class="footer">
      ⭐ Thank you for reviewing this project.
    </div>

  </div>
</body>
</html>

import { useNavigate } from "react-router-dom";
import axios from "axios";

const API = "http://127.0.0.1:8000";

function DashboardPage() {

  const navigate = useNavigate();
  const userId = 3;

  const connectGoogle = () => {
  window.location.href =
    `${API}/google/login/${userId}`;
};

const gmailCleanup = async () => {
  const res = await axios.post(
    `${API}/gmail/cleanup/${userId}`
  );

  alert(res.data.message);
};

const syncCalendar = async () => {
  const res = await axios.post(
    `${API}/calendar/create-event/${userId}`
  );

  alert(res.data.message);
};

const syncDrive = async () => {
  const res = await axios.post(
    `${API}/drive/create-folder/${userId}`
  );

  alert(res.data.message);
};

const runMailMind = async () => {
  const res = await axios.post(
    `${API}/mailmind/run/${userId}`
  );

  alert(res.data.message);
};

const downloadReport = () => {
  window.open(
    `${API}/mailmind/report`,
    "_blank"
  );
};
  return (
    <div className="dashboard">

      {/* HEADER */}

      <div className="dashboard-header">

        <div className="header-left">

          <img
            src="/mailmind_logo.png"
            alt="MailMind"
            className="dashboard-logo"
          />

          <div>
            <div className="workspace-tag">
              AI Productivity Workspace
            </div>
          </div>

        </div>

        <button
          className="logout-btn"
          onClick={() => navigate("/")}
        >
          Logout
        </button>

      </div>

      {/* WELCOME */}

      <div
        style={{
          marginBottom: "25px"
        }}
      >
        <h1
          style={{
            fontSize: "28px",
            fontWeight: "700",
            marginBottom: "8px"
          }}
        >
          Welcome back 👋
        </h1>

        <p
          style={{
            color: "#64748B"
          }}
        >
          Here's what's happening in your workspace today.
        </p>
      </div>

      {/* STATS */}

      <div className="stats-grid">

        <div className="stat-card">
          <h4>Events Detected</h4>
          <h2>12</h2>
        </div>

        <div className="stat-card">
          <h4>OTPs Deleted</h4>
          <h2>45</h2>
        </div>

        <div className="stat-card">
          <h4>Files Synced</h4>
          <h2>28</h2>
        </div>

        <div className="stat-card">
          <h4>Storage Used</h4>
          <h2>2.4GB</h2>
        </div>

      </div>

      {/* MAIN GRID */}

      <div className="dashboard-grid">

        <div className="panel">

          <h3>Quick Actions</h3>

          <button
            className="action-btn"
            onClick={connectGoogle}
          >
            🔗 Connect Google
          </button>
          <button
            className="action-btn"
            onClick={gmailCleanup}
          >
            📧 Gmail Cleanup
          </button>
          <button
            className="action-btn"
            onClick={syncCalendar}
          >
            📅 Sync Calendar
          </button>

          <button
            className="action-btn"
            onClick={syncDrive}
          >
            📁 Sync Drive
          </button>

          <button
            className="action-btn"
            onClick={downloadReport}
          >
            📄 Generate Report
          </button>
          <button
            className="action-btn"
            onClick={runMailMind}
          >
            🤖 Run MailMind
          </button>
        </div>

        <div className="panel">

          <h3>Recent Activity</h3>

          <ul className="activity-list">

            <li>
              🎯 Interview invitation detected
            </li>

            <li>
              📅 Calendar reminder created
            </li>

            <li>
              📧 12 OTP emails removed
            </li>

            <li>
              📁 Resume uploaded to Drive
            </li>

            <li>
              📊 Weekly productivity report generated
            </li>

          </ul>

        </div>

      </div>

      {/* SERVICES */}

      <div className="service-panel">

        <h3>Connected Services</h3>

        <div className="service-grid">

          <div className="service-card">
            <span>📧</span>
            Gmail Connected
          </div>

          <div className="service-card">
            <span>📅</span>
            Calendar Connected
          </div>

          <div className="service-card">
            <span>📁</span>
            Drive Connected
          </div>

        </div>

      </div>

      {/* AI SUMMARY */}

      <div
        className="service-panel"
        style={{ marginTop: "20px" }}
      >

        <h3>AI Summary</h3>

        <p
          style={{
            color: "#64748B",
            lineHeight: "1.8"
          }}
        >
          MailMind analyzed your mailbox, detected
          important calendar events, removed OTP
          clutter, synchronized Drive files and
          generated productivity insights to help
          you stay organized.
        </p>

      </div>

    </div>
  );
}

export default DashboardPage;
"use client";

import { useState, useEffect } from "react";
import {
  TextField,
  Button,
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  CircularProgress,
  Divider,
  Chip,
  LinearProgress,
  Snackbar,
  Alert,
} from "@mui/material";

export default function Home() {
  const [summary, setSummary] = useState("");
  const [results, setResults] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const [toast, setToast] = useState({ open: false, message: "", type: "success" });
  const [deletingId, setDeletingId] = useState(null);
  const [deletingAll, setDeletingAll] = useState(false);

  // ---------------- FETCH HISTORY ----------------
  const fetchHistory = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/history/");
      const data = await res.json();
      setHistory(data);
    } catch {
      console.log("History fetch error");
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  // ---------------- DELETE ONE ----------------
  const deleteItem = async (id) => {
    if (!confirm("Delete this record?")) return;

    setDeletingId(id);

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/history/delete/${id}/`,
        { method: "DELETE" }
      );

      if (!res.ok) throw new Error();

      setToast({ open: true, message: "Deleted successfully", type: "success" });
      fetchHistory();
    } catch {
      setToast({ open: true, message: "Delete failed", type: "error" });
    }

    setDeletingId(null);
  };

  // ---------------- DELETE ALL ----------------
  const deleteAllHistory = async () => {
    if (!confirm("Delete ALL history?")) return;

    setDeletingAll(true);

    try {
      const res = await fetch(
        "http://127.0.0.1:8000/history/delete-all/",
        { method: "DELETE" }
      );

      if (!res.ok) throw new Error();

      setToast({ open: true, message: "All history deleted", type: "success" });
      fetchHistory();
    } catch {
      setToast({ open: true, message: "Delete all failed", type: "error" });
    }

    setDeletingAll(false);
  };

  // ---------------- SUBMIT ----------------
  const handleSubmit = async () => {
    if (!summary.trim()) {
      setToast({ open: true, message: "Enter patient summary", type: "error" });
      return;
    }

    setLoading(true);
    setResults([]);

    const summaries = summary
      .split("\n")
      .filter((s) => s.trim() !== "");

    try {
      const res = await fetch("http://127.0.0.1:8000/analyze/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ summaries }),
      });

      const data = await res.json();
      setResults(data.results || []);
      fetchHistory();
    } catch {
      setToast({ open: true, message: "Backend error", type: "error" });
    }

    setLoading(false);
  };

  return (
    <>
      <Box
        sx={{
          minHeight: "100vh",
          background: "linear-gradient(135deg, #141E30 0%, #243B55 100%)",
          py: 5,
        }}
      >
        <Container maxWidth="md">

          {/* HEADER */}
          <Box textAlign="center" mb={4}>
            <Typography variant="h3" fontWeight="bold" color="white">
              🏥 Healthcare AI System
            </Typography>
            <Typography color="#bbb">
              Intelligent Diagnosis & Treatment Engine
            </Typography>
          </Box>

          {/* INPUT */}
          <Card sx={{ borderRadius: 4 }}>
            <CardContent>
              <TextField
                fullWidth
                multiline
                rows={4}
                label="Enter Patient Summaries (one per line)"
                value={summary}
                onChange={(e) => setSummary(e.target.value)}
              />

              <Button
                fullWidth
                variant="contained"
                size="large"
                sx={{ mt: 3, borderRadius: 3 }}
                onClick={handleSubmit}
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : "Analyze"}
              </Button>
            </CardContent>
          </Card>

          {/* RESULTS */}
          {results.length > 0 && (
            <Box mt={5}>
              {results.map((item, index) => (
                <Card key={index} sx={{ mb: 4, borderRadius: 3 }}>
                  <CardContent>

                    <Typography variant="h6">
                      🧑 Patient {index + 1}
                    </Typography>

                    <Typography mt={1}>
                      <b>Summary:</b> {item.summary}
                    </Typography>

                    <Box mt={2}>
                      <Typography><b>Diagnosis:</b> {item.diagnosis}</Typography>
                    </Box>

                    
                    {/* Risk */}
                    <Box mt={2}>
                      <Chip
                        label={item.risk}
                        color={
                          item.risk === "High"
                            ? "error"
                            : item.risk === "Medium"
                            ? "warning"
                            : "success"
                        }
                      />
                    </Box>

                    <Divider sx={{ my: 2 }} />

                    {/* Symptoms */}
                    <Box mt={2}>
                      <Typography><b>🩺 Symptoms:</b></Typography>
                      {item.symptoms?.map((s, i) => (
                        <Chip key={i} label={s} sx={{ mr: 1, mt: 1 }} />
                      ))}
                    </Box>

                    {/* ✅ CARE PLAN (MERGED) */}
                    {item.care_plan?.length > 0 && (
                      <Box mt={2}>
                        <Typography><b>💊 Care Plan:</b></Typography>
                        {item.care_plan.map((c, i) => (
                          <Typography key={i}>• {c}</Typography>
                        ))}
                      </Box>
                    )}

                    {/* ✅ TESTS (ONLY IF EXISTS) */}
                    {item.tests?.length > 0 && (
                      <Box mt={2}>
                        <Typography><b>🧪 Recommended Tests:</b></Typography>
                        {item.tests.map((t, i) => (
                          <Typography key={i}>• {t}</Typography>
                        ))}
                      </Box>
                    )}

                    {/* Emergency */}
                    <Box mt={2}>
                      <Typography color="error">
                        <b>🚨 Emergency:</b>
                      </Typography>
                      {item.emergency?.map((e, i) => (
                        <Typography key={i}>• {e}</Typography>
                      ))}
                    </Box>

                  </CardContent>
                </Card>
              ))}
            </Box>
          )}

          {/* HISTORY */}
          {history.length > 0 && (
            <Box mt={5}>
              <Typography variant="h5" color="white">
                📜 Recent History
              </Typography>

              <Button
                variant="contained"
                color="error"
                sx={{ mt: 2, mb: 2 }}
                onClick={deleteAllHistory}
                disabled={deletingAll}
              >
                {deletingAll ? <CircularProgress size={20} /> : "Delete All History"}
              </Button>

              {history.map((item) => (
                <Card key={item.id} sx={{ mt: 2, borderRadius: 3 }}>
                  <CardContent>
                    <Typography><b>Summary:</b> {item.summary}</Typography>
                    <Typography><b>Diagnosis:</b> {item.diagnosis}</Typography>
                    <Typography><b>Risk:</b> {item.risk}</Typography>

                    <Button
                      variant="outlined"
                      color="error"
                      sx={{ mt: 1 }}
                      onClick={() => deleteItem(item.id)}
                      disabled={deletingId === item.id}
                    >
                      {deletingId === item.id ? (
                        <CircularProgress size={20} />
                      ) : (
                        "Delete"
                      )}
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </Box>
          )}

        </Container>
      </Box>

      {/* TOAST */}
      <Snackbar
        open={toast.open}
        autoHideDuration={3000}
        onClose={() => setToast({ ...toast, open: false })}
      >
        <Alert
          severity={toast.type}
          onClose={() => setToast({ ...toast, open: false })}
          sx={{ width: "100%" }}
        >
          {toast.message}
        </Alert>
      </Snackbar>
    </>
  );
}
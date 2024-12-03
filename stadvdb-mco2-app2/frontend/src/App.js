import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import ConcurrencyControl from "./pages/ConcurrencyControl";
import CrashRecovery from "./pages/CrashRecovery";
import ConcurrencyRevised from "./pages/ConcurrencyRevised";

const App = () => {
    return (
        <Router>
            <div className="flex">
                {/* Sidebar */}
                <Sidebar />

                {/* Main Content */}
                <div className="flex-1 ml-64 p-6">
                    <Routes>
                        <Route path="/concurrency-control" element={<ConcurrencyRevised />} />
                        <Route path="/crash-recovery" element={<CrashRecovery />} />
                    </Routes>
                </div>
            </div>
        </Router>
    );
};

export default App;

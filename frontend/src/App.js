import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Header from './pages/Header';
import Footer from './pages/Footer';  // Importer le Footer
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import SurferForm from './pages/surfer/SurferForm';
import SurfClubForm from './pages/surfclub/SurfClubForm';
import SurfClubs from './pages/surfer/SurfClubs';
import SurfSpotDetails from './pages/surfer/SurfSpotDetails';
import Previsions from './pages/surfer/SurfSpotsList.jsx';
import Forum from './pages/surfer/Forum.jsx';
import Dashboard from './pages/surfclub/Dashboard.jsx';
import Monitors from './pages/surfclub/Monitors';
import Equipments from './pages/surfclub/Equipments';
import SurfSessions from './pages/surfclub/SurfSessions';
import LessonSchedules from './pages/surfclub/LessonSchedules';
import MonitorForm from './pages/surfclub/MonitorForm';
import SurfLessons from './pages/surfclub/SurfLessons';
import Orders from './pages/surfclub/Orders';
import SurfSessionForm from './pages/surfclub/SurfSessionForm';
import LessonScheduleForm from './pages/surfclub/LessonScheduleForm';
import Contact from './pages/Contact';
import OrderDetail from './pages/surfclub/OrderDetail';
import SurfClubDetails from './pages/surfer/SurfClubDetails';
import Accueil from './pages/Accueil';
import { UserProvider, useUser } from './context/UserContext';
import EquipmentForm from './pages/surfclub/EquipmentForm';
import SurfLessonDetail from './pages/surfclub/SurfLessonDetail';
import ReserveSession from './pages/surfer/ReserveSession';
import EquipmentDetails from './pages/surfer/EquipmentDetails';
import EquipmentList from './pages/surfer/EquipmentList';
import Cart from './pages/surfer/Cart';
import SpotsList from './pages/surfer/SpotsList';
import Forecast from './pages/surfer/Forecast';
import SurfSpotsList from './pages/surfer/SurfSpotsList';
import SurferProfile from './pages/surfer/SurferProfile';
import EditSurferProfile from './pages/surfer/EditSurferProfile';
import EditSurfClubProfile from './pages/surfclub/EditSurfClubProfile';
import SurfClubProfile from './pages/surfclub/SurfCubProfile';
import SurfClubStatistics from './pages/surfclub/SurfClubStatistics';
import Chatbot from './components/Chatbot';
import ChatbotButton from './components/ChatbotButton';

const App = () => {
  const { userRole, setUserRole } = useUser();

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      const role = localStorage.getItem('userRole');
      setUserRole(role); // Mettre à jour le contexte avec le rôle utilisateur
    }
  }, [setUserRole]);

  return (
    <Router>
      <ContentWithFooter userRole={userRole} setUserRole={setUserRole} />
    </Router>
  );
};

const ContentWithFooter = ({ userRole, setUserRole }) => {
  const location = useLocation(); // useLocation doit être utilisé ici après l'initialisation de Router
  const isDashboard = location.pathname.includes("/dashboard"); // Vérifie si c'est le dashboard
  const [isChatbotOpen, setIsChatbotOpen] = useState(false);

  // Fermer le chatbot et notifier les composants lors de la déconnexion
  useEffect(() => {
    if (!userRole) {
      setIsChatbotOpen(false);
      try { window.dispatchEvent(new CustomEvent('app:logout')); } catch (e) {}
    }
  }, [userRole]);

  return (
    <>
      <Header userRole={userRole} setUserRole={setUserRole} />
      <Routes>
        <Route path="/" element={<Accueil />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {userRole === 'surfer' && (
          <>
            <Route path="/surf-clubs" element={<SurfClubs />} />
            <Route path="/surf-spots/:id" element={<SurfSpotDetails />} />           
            <Route path="/previsions" element={<Previsions />} />
            <Route path="/forums" element={<SpotsList />} />
            <Route path="/surf-spots/:id" element={<SurfSpotDetails />} /> 
            <Route path="/surf-clubs/:id" element={<SurfClubDetails />} />
            <Route path="/reserve-session/:id" element={<ReserveSession />} />
            <Route path="/surf-clubs/:id/equipments" element={<EquipmentList />} />
            <Route path="/equipment/:equipmentId" element={<EquipmentDetails />} />
            <Route path="/cart" element={<Cart />} />
            <Route path="/forum/:surf_spot_id" element={<Forum />} />
            <Route path="/surf-spots" element={<SurfSpotsList />} />
            <Route path="/forecast/:spot_id" element={<Forecast />} />
            <Route path="/surfer/profile" element={<SurferProfile />} />
            <Route path="/surfer/edit" element={<EditSurferProfile />} />
          </>
        )}

        {userRole === 'surfclub' && (
          <>
            <Route path="/surfclub/profile" element={<SurfClubProfile />} />
            <Route path="/surfclub/edit" element={<EditSurfClubProfile />} />
            <Route path="/dashboard" element={<Dashboard />}>
              <Route path="monitors" element={<Monitors />} />
              <Route path="monitor/create" element={<MonitorForm />} />
              <Route path="monitor/:id/edit" element={<MonitorForm />} />
              <Route path="equipments" element={<Equipments />} />
              <Route path="equipment/create" element={<EquipmentForm />} />
              <Route path="equipment/:id/edit" element={<EquipmentForm />} />
              <Route path="surf-session" element={<SurfSessions />} />
              <Route path="/dashboard/surf-session/create" element={<SurfSessionForm />} />
              <Route path="/dashboard/surf-session/:id/edit" element={<SurfSessionForm />} />
              <Route path="lesson-schedule" element={<LessonSchedules />} />
              <Route path="/dashboard/lesson-schedule/create" element={<LessonScheduleForm />} />
              <Route path="/dashboard/lesson-schedule/:id/edit" element={<LessonScheduleForm />} />
              <Route path="surf-lesson" element={<SurfLessons />} />
              <Route path="/dashboard/surf-lesson/:id" element={<SurfLessonDetail />} />
              <Route path="orders" element={<Orders />} />
              <Route path="statistics" element={<SurfClubStatistics />} />
              <Route path="/dashboard/orders/:id" element={<OrderDetail />} />
              <Route path="statistics" element={<Orders />} />
            </Route>
          </>
        )}

        <Route path="*" element={<Navigate to="/" />} />
      </Routes>

      {/* Chatbot IA */}
      <ChatbotButton onClick={() => setIsChatbotOpen(true)} />
      <Chatbot isOpen={isChatbotOpen} onClose={() => setIsChatbotOpen(false)} />
      
      {/* Footer - affiché partout sauf sur le dashboard */}
      {!isDashboard && <Footer />}
    </>
  );
};

export default App;

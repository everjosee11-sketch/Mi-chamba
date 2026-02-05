import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Plus, X, LayoutDashboard, Users, 
  FileText, Wallet, CheckCircle2, AlertCircle, 
  ChevronRight, HardHat, TrendingUp 
} from 'lucide-react';

// --- COMPONENTE DE ENTRADA DE DATOS (FORMULARIO FUTURISTA) ---
const ModalForm = ({ isOpen, onClose, onAdd }) => {
  const [formData, setFormData] = useState({
    nombre: '', presupuesto: '', personal: '', art: 'Al día', avance: 0
  });

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
      <motion.div 
        initial={{ opacity: 0, scale: 0.9, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        className="bg-[#0d1117] border border-cyan-500/30 p-8 rounded-3xl w-full max-w-md shadow-[0_0_40px_rgba(34,211,238,0.15)]"
      >
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-cyan-400 font-light tracking-[0.2em] uppercase">Nuevo Registro</h2>
          <button onClick={onClose} className="text-white/40 hover:text-white"><X size={20}/></button>
        </div>

        <div className="space-y-4">
          <div>
            <label className="text-[10px] text-white/40 uppercase ml-2">Nombre del Proyecto</label>
            <input 
              className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 mt-1 focus:border-cyan-500 outline-none transition-all"
              onChange={(e) => setFormData({...formData, nombre: e.target.value})}
              placeholder="Ej. Torre Central"
            />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-[10px] text-white/40 uppercase ml-2">Presupuesto ($)</label>
              <input 
                type="number"
                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 mt-1 focus:border-cyan-500 outline-none transition-all"
                onChange={(e) => setFormData({...formData, presupuesto: e.target.value})}
              />
            </div>
            <div>
              <label className="text-[10px] text-white/40 uppercase ml-2">Personal</label>
              <input 
                type="number"
                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 mt-1 focus:border-cyan-500 outline-none transition-all"
                onChange={(e) => setFormData({...formData, personal: e.target.value})}
              />
            </div>
          </div>
          <button 
            onClick={() => { onAdd(formData); onClose(); }}
            className="w-full bg-cyan-600 hover:bg-cyan-500 text-black font-bold py-4 rounded-xl mt-4 transition-all uppercase tracking-widest text-xs"
          >
            Sincronizar Datos
          </button>
        </div>
      </motion.div>
    </div>
  );
};

// --- APLICACIÓN PRINCIPAL ---
export default function CoreApp() {
  const [proyectos, setProyectos] = useState([
    { id: 1, nombre: "Mantenimiento ART-01", presupuesto: 45000, personal: 8, art: "Vigente", avance: 85 },
    { id: 2, nombre: "Infraestructura Red", presupuesto: 120000, personal: 24, art: "Pendiente", avance: 30 }
  ]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [totalBudget, setTotalBudget] = useState(0);

  // Cálculo automático del motor
  useEffect(() => {
    const total = proyectos.reduce((acc, curr) => acc + Number(curr.presupuesto), 0);
    setTotalBudget(total);
  }, [proyectos]);

  const agregarProyecto = (nuevo) => {
    setProyectos([...proyectos, { ...nuevo, id: proyectos.length + 1 }]);
  };

  return (
    <div className="min-h-screen bg-[#02040a] text-slate-300 font-sans selection:bg-cyan-500/30">
      {/* Fondo Animado */}
      <div className="fixed inset-0 overflow-hidden -z-10">
        <div className="absolute top-[-10%] right-[-5%] w-96 h-96 bg-cyan-600/10 rounded-full blur-[120px]" />
        <div className="absolute bottom-[-10%] left-[-5%] w-96 h-96 bg-purple-600/10 rounded-full blur-[120px]" />
      </div>

      <div className="max-w-7xl mx-auto p-6 lg:p-12">
        {/* Header Superior */}
        <header className="flex justify-between items-start mb-16">
          <div>
            <h1 className="text-5xl font-thin tracking-tighter text-white italic">CORE<span className="text-cyan-500 font-bold not-italic">.</span></h1>
            <p className="text-[10px] tracking-[0.5em] text-cyan-500/50 uppercase mt-2">Enterprise Control System</p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-mono text-white">${totalBudget.toLocaleString()}</div>
            <div className="text-[10px] text-white/30 uppercase tracking-widest">Capital en Gestión</div>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
          {/* Navegación Lateral */}
          <aside className="lg:col-span-3 space-y-2">
            {[
              { label: 'Proyectos', icon: LayoutDashboard, active: true },
              { label: 'Personal / ART', icon: HardHat, active: false },
              { label: 'Presupuestos', icon: Wallet, active: false },
              { label: 'Archivos', icon: FileText, active: false }
            ].map((item, i) => (
              <div 
                key={i}
                className={`flex items-center gap-4 p-4 rounded-2xl cursor-pointer transition-all ${item.active ? 'bg-white/10 border border-white/10 text-white' : 'hover:bg-white/5 text-white/40'}`}
              >
                <item.icon size={18} className={item.active ? 'text-cyan-400' : ''}/>
                <span className="text-xs uppercase tracking-[0.2em]">{item.label}</span>
              </div>
            ))}
          </aside>

          {/* Panel Central */}
          <main className="lg:col-span-9 space-y-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-light uppercase tracking-widest">Monitor de Operaciones</h2>
              <button 
                onClick={() => setIsModalOpen(true)}
                className="flex items-center gap-2 px-5 py-2 bg-cyan-500/10 border border-cyan-500/50 rounded-full text-cyan-400 text-xs hover:bg-cyan-500 hover:text-black transition-all"
              >
                <Plus size={14}/> Nuevo Proyecto
              </button>
            </div>

            <div className="grid gap-4">
              <AnimatePresence>
                {proyectos.map((p) => (
                  <motion.div 
                    key={p.id}
                    layout
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="group bg-white/5 border border-white/5 p-6 rounded-3xl flex flex-wrap items-center justify-between gap-6 hover:bg-white/[0.08] hover:border-cyan-500/30 transition-all"
                  >
                    <div className="flex items-center gap-6">
                      <div className={`p-3 rounded-2xl bg-black/40 border ${p.avance === 100 ? 'border-emerald-500/50' : 'border-white/10'}`}>
                        {p.avance === 100 ? <CheckCircle2 className="text-emerald-500" /> : <TrendingUp className="text-cyan-400" />}
                      </div>
                      <div>
                        <h3 className="text-white font-medium">{p.nombre}</h3>
                        <p className="text-[10px] text-white/30 uppercase tracking-widest">Operarios: {p.personal} | ART: {p.art}</p>
                      </div>
                    </div>

                    <div className="flex-1 max-w-[200px] hidden md:block px-8">
                      <div className="h-[2px] w-full bg-white/10 rounded-full overflow-hidden">
                        <motion.div 
                          initial={{ width: 0 }}
                          animate={{ width: `${p.avance}%` }}
                          className="h-full bg-gradient-to-r from-cyan-500 to-blue-500"
                        />
                      </div>
                    </div>

                    <div className="text-right">
                      <span className="text-sm font-mono text-white">${Number(p.presupuesto).toLocaleString()}</span>
                      <div className="text-[10px] text-cyan-400/50 uppercase tracking-tighter mt-1">{p.avance}% Completado</div>
                    </div>
                    <ChevronRight className="text-white/10 group-hover:text-cyan-500" size={20}/>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          </main>
        </div>
      </div>

      <ModalForm 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        onAdd={agregarProyecto}
      />
    </div>
  );
}

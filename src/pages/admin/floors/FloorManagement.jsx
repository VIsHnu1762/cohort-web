import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Building2, Users, UserCheck, Plus, Edit2, Trash2, Save, X } from 'lucide-react';
import GlassCard from '../../../components/GlassCard';
import Button from '../../../components/Button';
import Input from '../../../components/Input';
import './FloorManagement.css';

const FloorManagement = () => {
    const [floors, setFloors] = useState([
        {
            id: 1,
            name: 'Floor A',
            mentors: ['Reshma', 'Gopi'],
            students: 28,
            performance: 85,
            color: '#4CAF50'
        },
        {
            id: 2,
            name: 'Floor B',
            mentors: ['Reshma'],
            students: 25,
            performance: 78,
            color: '#2196F3'
        },
        {
            id: 3,
            name: 'Floor C',
            mentors: ['Thulasi'],
            students: 22,
            performance: 92,
            color: '#ffcc00'
        },
        {
            id: 4,
            name: 'Floor D',
            mentors: ['Thulasi'],
            students: 20,
            performance: 75,
            color: '#9C27B0'
        },
        {
            id: 5,
            name: 'Floor E',
            mentors: ['Gopi'],
            students: 25,
            performance: 88,
            color: '#FF9800'
        }
    ]);

    const [isAddingFloor, setIsAddingFloor] = useState(false);
    const [editingFloor, setEditingFloor] = useState(null);
    const [newFloor, setNewFloor] = useState({ name: '', mentors: [], students: 0, color: '#4CAF50' });

    const allMentors = ['Reshma', 'Thulasi', 'Gopi'];

    const handleAddFloor = () => {
        if (newFloor.name) {
            setFloors([...floors, { ...newFloor, id: floors.length + 1, performance: 0 }]);
            setNewFloor({ name: '', mentors: [], students: 0, color: '#4CAF50' });
            setIsAddingFloor(false);
        }
    };

    const handleDeleteFloor = (id) => {
        setFloors(floors.filter(f => f.id !== id));
    };

    const handleEditFloor = (floor) => {
        setEditingFloor({ ...floor });
    };

    const handleSaveEdit = () => {
        setFloors(floors.map(f => f.id === editingFloor.id ? editingFloor : f));
        setEditingFloor(null);
    };

    const toggleMentor = (mentor, floorData, setter) => {
        const mentors = floorData.mentors.includes(mentor)
            ? floorData.mentors.filter(m => m !== mentor)
            : [...floorData.mentors, mentor];
        setter({ ...floorData, mentors });
    };

    return (
        <div className="floor-management-page">
            <div className="page-header">
                <div>
                    <h1 className="page-title">Floor Management</h1>
                    <p className="page-subtitle">Organize students into floors and assign mentors</p>
                </div>
                <Button variant="primary" onClick={() => setIsAddingFloor(true)}>
                    <Plus size={18} />
                    Add New Floor
                </Button>
            </div>

            {/* Add New Floor Form */}
            {isAddingFloor && (
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <GlassCard className="floor-form-card">
                        <h3>Add New Floor</h3>
                        <div className="floor-form">
                            <Input
                                label="Floor Name"
                                placeholder="e.g., Floor F"
                                value={newFloor.name}
                                onChange={(e) => setNewFloor({ ...newFloor, name: e.target.value })}
                            />
                            <div className="form-group">
                                <label>Assign Mentors</label>
                                <div className="mentor-checkboxes">
                                    {allMentors.map(mentor => (
                                        <label key={mentor} className="checkbox-label">
                                            <input
                                                type="checkbox"
                                                checked={newFloor.mentors.includes(mentor)}
                                                onChange={() => toggleMentor(mentor, newFloor, setNewFloor)}
                                            />
                                            {mentor}
                                        </label>
                                    ))}
                                </div>
                            </div>
                            <div className="form-group">
                                <label>Floor Color</label>
                                <input
                                    type="color"
                                    value={newFloor.color}
                                    onChange={(e) => setNewFloor({ ...newFloor, color: e.target.value })}
                                    className="color-picker"
                                />
                            </div>
                            <div className="form-actions">
                                <Button variant="primary" onClick={handleAddFloor}>
                                    <Save size={18} />
                                    Save Floor
                                </Button>
                                <Button variant="secondary" onClick={() => setIsAddingFloor(false)}>
                                    <X size={18} />
                                    Cancel
                                </Button>
                            </div>
                        </div>
                    </GlassCard>
                </motion.div>
            )}

            {/* Floors Grid */}
            <div className="floors-grid">
                {floors.map((floor) => (
                    <motion.div
                        key={floor.id}
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        whileHover={{ scale: 1.02 }}
                    >
                        <GlassCard className="floor-card">
                            {editingFloor && editingFloor.id === floor.id ? (
                                <div className="floor-edit-form">
                                    <Input
                                        label="Floor Name"
                                        value={editingFloor.name}
                                        onChange={(e) => setEditingFloor({ ...editingFloor, name: e.target.value })}
                                    />
                                    <div className="form-group">
                                        <label>Assign Mentors</label>
                                        <div className="mentor-checkboxes">
                                            {allMentors.map(mentor => (
                                                <label key={mentor} className="checkbox-label">
                                                    <input
                                                        type="checkbox"
                                                        checked={editingFloor.mentors.includes(mentor)}
                                                        onChange={() => toggleMentor(mentor, editingFloor, setEditingFloor)}
                                                    />
                                                    {mentor}
                                                </label>
                                            ))}
                                        </div>
                                    </div>
                                    <div className="form-actions">
                                        <Button variant="success" onClick={handleSaveEdit}>
                                            <Save size={16} />
                                            Save
                                        </Button>
                                        <Button variant="secondary" onClick={() => setEditingFloor(null)}>
                                            <X size={16} />
                                            Cancel
                                        </Button>
                                    </div>
                                </div>
                            ) : (
                                <>
                                    <div className="floor-header" style={{ borderLeftColor: floor.color }}>
                                        <h3>{floor.name}</h3>
                                        <div className="floor-actions">
                                            <button
                                                className="icon-button"
                                                onClick={() => handleEditFloor(floor)}
                                                title="Edit Floor"
                                            >
                                                <Edit2 size={18} />
                                            </button>
                                            <button
                                                className="icon-button danger"
                                                onClick={() => handleDeleteFloor(floor.id)}
                                                title="Delete Floor"
                                            >
                                                <Trash2 size={18} />
                                            </button>
                                        </div>
                                    </div>

                                    <div className="floor-stats">
                                        <div className="stat-item">
                                            <Users size={24} color={floor.color} />
                                            <div>
                                                <p className="stat-value">{floor.students}</p>
                                                <p className="stat-label">Students</p>
                                            </div>
                                        </div>
                                        <div className="stat-item">
                                            <UserCheck size={24} color={floor.color} />
                                            <div>
                                                <p className="stat-value">{floor.mentors.length}</p>
                                                <p className="stat-label">Mentors</p>
                                            </div>
                                        </div>
                                    </div>

                                    <div className="floor-mentors">
                                        <label>Assigned Mentors:</label>
                                        <div className="mentor-tags">
                                            {floor.mentors.map(mentor => (
                                                <span key={mentor} className="mentor-tag" style={{ backgroundColor: `${floor.color}20`, color: floor.color }}>
                                                    {mentor}
                                                </span>
                                            ))}
                                        </div>
                                    </div>

                                    <div className="floor-performance">
                                        <label>Performance Score</label>
                                        <div className="performance-bar">
                                            <div
                                                className="performance-fill"
                                                style={{ width: `${floor.performance}%`, backgroundColor: floor.color }}
                                            >
                                                <span>{floor.performance}%</span>
                                            </div>
                                        </div>
                                    </div>
                                </>
                            )}
                        </GlassCard>
                    </motion.div>
                ))}
            </div>
        </div>
    );
};

export default FloorManagement;

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
    Save, Plus, Trash2, Edit2, BookOpen, Award, 
    CheckCircle, AlertCircle, Settings, ChevronDown, ChevronUp
} from 'lucide-react';
import StatCard from '../../../components/admin/StatCard';
import Modal from '../../../components/admin/Modal';
import { pillarRulesData } from '../../../data/mockAdminData';

const PillarRulesConfig = () => {
    const [rules, setRules] = useState(pillarRulesData);
    const [selectedPillar, setSelectedPillar] = useState('CLT');
    const [expandedRule, setExpandedRule] = useState(null);
    const [isEditModalOpen, setIsEditModalOpen] = useState(false);
    const [editingRule, setEditingRule] = useState(null);
    const [isAddingRule, setIsAddingRule] = useState(false);

    const pillars = ['CLT', 'SRI', 'CFC', 'IIPC', 'SCD'];
    const pillarColors = {
        CLT: 'indigo',
        SRI: 'purple',
        CFC: 'pink',
        IIPC: 'green',
        SCD: 'amber'
    };

    // Get rules for selected pillar
    const currentPillarRules = rules.filter(r => r.pillar === selectedPillar);

    // Calculate stats
    const totalRules = rules.length;
    const activeRules = rules.filter(r => r.isActive).length;
    const totalXPAvailable = rules.reduce((sum, r) => sum + r.xpReward, 0);

    // Handle edit rule
    const handleEditRule = (rule) => {
        setEditingRule({ ...rule });
        setIsAddingRule(false);
        setIsEditModalOpen(true);
    };

    // Handle add new rule
    const handleAddRule = () => {
        setEditingRule({
            id: Date.now(),
            pillar: selectedPillar,
            title: '',
            description: '',
            xpReward: 100,
            difficulty: 'Medium',
            isActive: true,
            requirements: []
        });
        setIsAddingRule(true);
        setIsEditModalOpen(true);
    };

    // Handle save rule
    const handleSaveRule = () => {
        if (isAddingRule) {
            setRules([...rules, editingRule]);
        } else {
            setRules(rules.map(r => r.id === editingRule.id ? editingRule : r));
        }
        setIsEditModalOpen(false);
        setEditingRule(null);
    };

    // Handle delete rule
    const handleDeleteRule = (ruleId) => {
        if (confirm('Are you sure you want to delete this rule?')) {
            setRules(rules.filter(r => r.id !== ruleId));
        }
    };

    // Handle toggle rule active status
    const handleToggleActive = (ruleId) => {
        setRules(rules.map(r => 
            r.id === ruleId ? { ...r, isActive: !r.isActive } : r
        ));
    };

    // Difficulty badge
    const DifficultyBadge = ({ difficulty }) => {
        const colors = {
            Easy: 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400',
            Medium: 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400',
            Hard: 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
        };
        return (
            <span className={`px-2 py-1 rounded text-xs font-medium ${colors[difficulty]}`}>
                {difficulty}
            </span>
        );
    };

    return (
        <div className="p-6 min-h-screen">
            {/* Header */}
            <div className="mb-8">
                <div className="flex items-center justify-between mb-4">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                            Pillar Rules Configuration
                        </h1>
                        <p className="text-gray-600 dark:text-gray-400">
                            Manage rules, requirements, and XP rewards for all pillars
                        </p>
                    </div>
                    <button
                        onClick={handleAddRule}
                        className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                    >
                        <Plus size={20} />
                        Add Rule
                    </button>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <StatCard
                        title="Total Rules"
                        value={totalRules}
                        icon={BookOpen}
                        iconColor="bg-indigo-600"
                    />
                    <StatCard
                        title="Active Rules"
                        value={activeRules}
                        icon={CheckCircle}
                        iconColor="bg-green-600"
                    />
                    <StatCard
                        title="Total XP Available"
                        value={totalXPAvailable.toLocaleString()}
                        icon={Award}
                        iconColor="bg-purple-600"
                    />
                    <StatCard
                        title="Pillars Configured"
                        value={pillars.length}
                        icon={Settings}
                        iconColor="bg-amber-600"
                    />
                </div>
            </div>

            {/* Pillar Selector */}
            <div className="glass-card p-4 mb-6">
                <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-3">
                    Select Pillar
                </h3>
                <div className="flex flex-wrap gap-3">
                    {pillars.map(pillar => {
                        const color = pillarColors[pillar];
                        const pillarRulesCount = rules.filter(r => r.pillar === pillar).length;
                        const pillarActiveCount = rules.filter(r => r.pillar === pillar && r.isActive).length;
                        
                        return (
                            <button
                                key={pillar}
                                onClick={() => setSelectedPillar(pillar)}
                                className={`flex-1 min-w-[150px] p-4 rounded-lg border-2 transition-all ${
                                    selectedPillar === pillar
                                        ? `border-${color}-500 bg-${color}-50 dark:bg-${color}-900/20`
                                        : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
                                }`}
                            >
                                <div className="text-center">
                                    <p className={`text-xl font-bold ${
                                        selectedPillar === pillar 
                                            ? `text-${color}-600 dark:text-${color}-400`
                                            : 'text-gray-900 dark:text-white'
                                    }`}>
                                        {pillar}
                                    </p>
                                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                                        {pillarActiveCount}/{pillarRulesCount} active
                                    </p>
                                </div>
                            </button>
                        );
                    })}
                </div>
            </div>

            {/* Rules List */}
            <div className="space-y-4">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                        {selectedPillar} Rules ({currentPillarRules.length})
                    </h2>
                </div>

                {currentPillarRules.length === 0 ? (
                    <div className="glass-card p-12 text-center">
                        <AlertCircle size={48} className="mx-auto text-gray-400 mb-4" />
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                            No Rules Configured
                        </h3>
                        <p className="text-gray-600 dark:text-gray-400 mb-4">
                            Add your first rule for {selectedPillar} pillar
                        </p>
                        <button
                            onClick={handleAddRule}
                            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                        >
                            Add Rule
                        </button>
                    </div>
                ) : (
                    currentPillarRules.map((rule, index) => (
                        <motion.div
                            key={rule.id}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.05 }}
                            className={`glass-card p-6 ${
                                !rule.isActive ? 'opacity-60' : ''
                            }`}
                        >
                            {/* Rule Header */}
                            <div className="flex items-start justify-between mb-4">
                                <div className="flex-1">
                                    <div className="flex items-center gap-3 mb-2">
                                        <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                                            {rule.title}
                                        </h3>
                                        <DifficultyBadge difficulty={rule.difficulty} />
                                        {!rule.isActive && (
                                            <span className="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400 rounded text-xs font-medium">
                                                Inactive
                                            </span>
                                        )}
                                    </div>
                                    <p className="text-gray-600 dark:text-gray-400">
                                        {rule.description}
                                    </p>
                                </div>
                                <div className="flex items-center gap-2 ml-4">
                                    <div className="text-right mr-4">
                                        <div className="flex items-center gap-1 text-purple-600 dark:text-purple-400">
                                            <Award size={18} />
                                            <span className="font-bold text-lg">{rule.xpReward}</span>
                                        </div>
                                        <p className="text-xs text-gray-500 dark:text-gray-400">XP Reward</p>
                                    </div>
                                    <button
                                        onClick={() => handleEditRule(rule)}
                                        className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                                        title="Edit Rule"
                                    >
                                        <Edit2 size={18} className="text-gray-600 dark:text-gray-400" />
                                    </button>
                                    <button
                                        onClick={() => handleToggleActive(rule.id)}
                                        className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                                        title={rule.isActive ? 'Deactivate' : 'Activate'}
                                    >
                                        <CheckCircle 
                                            size={18} 
                                            className={rule.isActive ? 'text-green-600' : 'text-gray-400'} 
                                        />
                                    </button>
                                    <button
                                        onClick={() => handleDeleteRule(rule.id)}
                                        className="p-2 hover:bg-red-100 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                                        title="Delete Rule"
                                    >
                                        <Trash2 size={18} className="text-red-600 dark:text-red-400" />
                                    </button>
                                    <button
                                        onClick={() => setExpandedRule(expandedRule === rule.id ? null : rule.id)}
                                        className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                                    >
                                        {expandedRule === rule.id ? (
                                            <ChevronUp size={18} className="text-gray-600 dark:text-gray-400" />
                                        ) : (
                                            <ChevronDown size={18} className="text-gray-600 dark:text-gray-400" />
                                        )}
                                    </button>
                                </div>
                            </div>

                            {/* Expanded Requirements */}
                            {expandedRule === rule.id && rule.requirements && rule.requirements.length > 0 && (
                                <motion.div
                                    initial={{ opacity: 0, height: 0 }}
                                    animate={{ opacity: 1, height: 'auto' }}
                                    exit={{ opacity: 0, height: 0 }}
                                    className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700"
                                >
                                    <h4 className="font-semibold text-gray-900 dark:text-white mb-3">
                                        Requirements:
                                    </h4>
                                    <ul className="space-y-2">
                                        {rule.requirements.map((req, idx) => (
                                            <li key={idx} className="flex items-start gap-2">
                                                <CheckCircle size={16} className="text-green-500 mt-1 flex-shrink-0" />
                                                <span className="text-gray-700 dark:text-gray-300">{req}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </motion.div>
                            )}
                        </motion.div>
                    ))
                )}
            </div>

            {/* Edit/Add Rule Modal */}
            <Modal
                isOpen={isEditModalOpen}
                onClose={() => {
                    setIsEditModalOpen(false);
                    setEditingRule(null);
                }}
                title={isAddingRule ? 'Add New Rule' : 'Edit Rule'}
                size="lg"
            >
                {editingRule && (
                    <div className="space-y-4">
                        {/* Pillar Selection */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                Pillar
                            </label>
                            <select
                                value={editingRule.pillar}
                                onChange={(e) => setEditingRule({ ...editingRule, pillar: e.target.value })}
                                className="w-full px-3 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                disabled={!isAddingRule}
                            >
                                {pillars.map(pillar => (
                                    <option key={pillar} value={pillar}>{pillar}</option>
                                ))}
                            </select>
                        </div>

                        {/* Title */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                Rule Title
                            </label>
                            <input
                                type="text"
                                value={editingRule.title}
                                onChange={(e) => setEditingRule({ ...editingRule, title: e.target.value })}
                                className="w-full px-3 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                placeholder="e.g., LinkedIn Profile Optimization"
                            />
                        </div>

                        {/* Description */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                Description
                            </label>
                            <textarea
                                value={editingRule.description}
                                onChange={(e) => setEditingRule({ ...editingRule, description: e.target.value })}
                                rows={3}
                                className="w-full px-3 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                placeholder="Describe what students need to do..."
                            />
                        </div>

                        {/* XP Reward and Difficulty */}
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                    XP Reward
                                </label>
                                <input
                                    type="number"
                                    value={editingRule.xpReward}
                                    onChange={(e) => setEditingRule({ ...editingRule, xpReward: parseInt(e.target.value) || 0 })}
                                    className="w-full px-3 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                    min="0"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                    Difficulty
                                </label>
                                <select
                                    value={editingRule.difficulty}
                                    onChange={(e) => setEditingRule({ ...editingRule, difficulty: e.target.value })}
                                    className="w-full px-3 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                >
                                    <option value="Easy">Easy</option>
                                    <option value="Medium">Medium</option>
                                    <option value="Hard">Hard</option>
                                </select>
                            </div>
                        </div>

                        {/* Active Status */}
                        <div className="flex items-center gap-2">
                            <input
                                type="checkbox"
                                id="isActive"
                                checked={editingRule.isActive}
                                onChange={(e) => setEditingRule({ ...editingRule, isActive: e.target.checked })}
                                className="w-4 h-4 text-indigo-600 rounded focus:ring-2 focus:ring-indigo-500"
                            />
                            <label htmlFor="isActive" className="text-sm font-medium text-gray-700 dark:text-gray-300">
                                Rule is active
                            </label>
                        </div>

                        {/* Requirements */}
                        <div>
                            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                                Requirements (one per line)
                            </label>
                            <textarea
                                value={editingRule.requirements?.join('\n') || ''}
                                onChange={(e) => setEditingRule({ 
                                    ...editingRule, 
                                    requirements: e.target.value.split('\n').filter(r => r.trim()) 
                                })}
                                rows={4}
                                className="w-full px-3 py-2 bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500"
                                placeholder="Complete profile sections&#10;Add professional headline&#10;Upload profile photo"
                            />
                        </div>

                        {/* Actions */}
                        <div className="flex gap-3 pt-4">
                            <button
                                onClick={handleSaveRule}
                                className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                            >
                                <Save size={18} />
                                {isAddingRule ? 'Add Rule' : 'Save Changes'}
                            </button>
                            <button
                                onClick={() => setIsEditModalOpen(false)}
                                className="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
                            >
                                Cancel
                            </button>
                        </div>
                    </div>
                )}
            </Modal>
        </div>
    );
};

export default PillarRulesConfig;

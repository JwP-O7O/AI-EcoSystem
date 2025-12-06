import React from 'react';
import { PricingTier } from './types';

export const ICONS = {
    CHEVRON_RIGHT: <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" /></svg>,
    CHECK: <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>,
    CODE: <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-brand-accent-start" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l-4 4-4-4M6 16l-4-4 4-4" /></svg>,
    CUBE: <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-brand-accent-start" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>,
    COMMAND: <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-brand-accent-start" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 9l4-4 4 4m0 6l-4 4-4-4" /></svg>,
    SPARKLES: <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-14l-1 1m6 0l-1-1m-4 4l1-1m-1 6l1 1M6 21a9 9 0 0118 0H6z" /></svg>,
    GEAR: <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924-1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>,
    TERMINAL: <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M8 9l4-4 4 4m0 6l-4 4-4-4" /></svg>,
    DASHBOARD: <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>,
    AGENTS: <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>,
    LOGOUT: <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>,
};

export const PRICING_TIERS: PricingTier[] = [
    {
        id: 'scout_agent',
        name: 'Scout Agent',
        description: 'Een capabele agent voor specifieke, geautomatiseerde taken.',
        price: 799,
        features: [
            'Keuze uit alle standaard bot types',
            'Basis Q&A en commandoverwerking',
            'Eenvoudige integratie',
            'Community & e-mailondersteuning'
        ],
    },
    {
        id: 'hunter_agent',
        name: 'Hunter Agent',
        description: 'Een geavanceerde agent met proactieve vaardigheden en tools.',
        price: 1799,
        isPopular: true,
        features: [
            'Alle Scout Agent-functies',
            'Gebruik van geavanceerde tools (Web Search)',
            'Lange-termijn geheugen',
            'Prioritaire e-mail & chatondersteuning',
            'Analytics-dashboard'
        ],
    },
    {
        id: 'apex_agent',
        name: 'Apex Agent',
        description: 'Een elite, volledig autonome agent voor complexe bedrijfsprocessen.',
        price: 5499,
        features: [
            'Alle Hunter Agent-functies',
            'Geavanceerde tool-chaining',
            'API-integratie en bestandsinteractie',
            'Mogelijkheid tot geplande executie',
            'Toegewijde accountmanager'
        ],
    },
];

export const BUILDER_OPTIONS = {
    botTypes: [
        { name: 'Gespreks-AI', price: 200, description: "Voert gesprekken en beantwoordt vragen." },
        { name: 'Data Analyse Bot', price: 650, description: "Analyseert datasets en genereert inzichten." },
        { name: 'Content Creatie Bot', price: 550, description: "Schrijft artikelen, e-mails of social media posts." },
        { name: 'Trading Bot', price: 750, description: "Analyseert markten en voert transacties uit." },
        { name: 'Web Scraper Bot', price: 450, description: "Extraheert gestructureerde data van websites." },
        { name: 'Email Automation Bot', price: 400, description: "Automatiseert het versturen van e-mails." },
    ],
    tradingTactics: [
        { name: 'RSI Crossover', price: 200, description: "Handelt op basis van de Relative Strength Index." },
        { name: 'MACD Strategie', price: 200, description: "Gebruikt de Moving Average Convergence Divergence." },
        { name: 'Bollinger Bands', price: 250, description: "Handelt op basis van marktvolatiliteit." },
        { name: 'Ichimoku Cloud', price: 350, description: "Geavanceerde alles-in-één indicator." },
    ],
    features: [
        { name: 'Real-time Web Search', price: 350, description: "Kan live op het web zoeken voor actuele info." },
        { name: 'Lange-termijn Geheugen', price: 150, description: "Onthoudt eerdere interacties." },
        { name: 'Bestandsinteractie (Lezen/Schrijven)', price: 300, description: "Kan bestanden lezen en schrijven." },
        { name: 'API Integratie', price: 400, description: "Maakt verbinding met externe diensten." },
        { name: 'Tool Gebruik (Calculator)', price: 100, description: "Kan basisberekeningen uitvoeren." },
        { name: 'Geplande Executie', price: 250, description: "Kan taken op gezette tijden uitvoeren." },
    ],
    personalities: [
        'Professioneel',
        'Vriendelijk & Behulpzaam',
        'Geestig & Creatief',
        'Direct & To-the-point',
        'Analytisch & Data-gedreven'
    ]
};
import React, { useState } from 'react';
import { GeneratedFile } from '../types';

interface GeneratedFileViewerProps {
    files: GeneratedFile[];
}

const GeneratedFileViewer: React.FC<GeneratedFileViewerProps> = ({ files }) => {
    const [activeIndex, setActiveIndex] = useState(0);
    const [copySuccess, setCopySuccess] = useState('');

    const handleCopy = () => {
        navigator.clipboard.writeText(files[activeIndex].content).then(() => {
            setCopySuccess('Gekopieerd!');
            setTimeout(() => setCopySuccess(''), 2000);
        }, (err) => {
            setCopySuccess('Kopiëren mislukt');
            console.error('Kon tekst niet kopiëren: ', err);
        });
    };
    
    if (!files || files.length === 0) {
        return null;
    }

    return (
        <div className="bg-brand-primary border border-slate-700 rounded-lg mt-8 w-full text-left">
            {/* Tabs */}
            <div className="flex border-b border-slate-700 flex-wrap">
                {files.map((file, index) => (
                    <button
                        key={file.filename}
                        onClick={() => setActiveIndex(index)}
                        className={`px-4 py-2 text-sm font-medium transition-colors ${
                            activeIndex === index
                                ? 'bg-brand-secondary text-white border-b-2 border-indigo-500'
                                : 'text-slate-400 hover:bg-slate-800/50'
                        }`}
                    >
                        {file.filename}
                    </button>
                ))}
            </div>

            {/* Content */}
            <div className="relative p-4">
                 <button 
                    onClick={handleCopy}
                    className="absolute top-6 right-4 bg-slate-600 hover:bg-slate-500 text-white text-xs font-semibold px-2 py-1 rounded transition-colors"
                >
                    {copySuccess || 'Kopieer Code'}
                </button>
                <pre className="text-sm bg-transparent rounded-b-lg overflow-x-auto">
                    <code className="language-python text-slate-300">
                        {files[activeIndex].content}
                    </code>
                </pre>
            </div>
        </div>
    );
};

export default GeneratedFileViewer;
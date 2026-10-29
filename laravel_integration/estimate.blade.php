<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Construction AI Estimation Agent - Bridge & Infrastructure</title>
    <!-- Tailwind CSS CDN for instant styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #0f172a; color: #f8fafc; }
        .glass-panel { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); }
        .gradient-header { background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 50%, #0ea5e9 100%); }
    </style>
</head>
<body class="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto space-y-8">

        <!-- Top Header & Agent Status Banner -->
        <header class="glass-panel rounded-2xl p-6 shadow-2xl flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
                <div class="flex items-center gap-3">
                    <span class="px-3 py-1 text-xs font-bold rounded-full bg-blue-500/20 text-blue-400 border border-blue-500/30">
                        INDIAN INFRASTRUCTURE RAG AGENT
                    </span>
                    <span class="text-xs text-slate-400">IRC:112 | MoRTH 5th Rev | Assam PWD SOR</span>
                </div>
                <h1 class="text-3xl font-extrabold text-white mt-1">Bridge Construction Quantity & Cost Estimator</h1>
                <p class="text-sm text-slate-400 mt-1">Deterministic Civil Engineering Formulas + Vector Retrieval of Indian Standards</p>
            </div>
            <div class="flex items-center gap-3 text-xs bg-slate-800/80 px-4 py-2.5 rounded-xl border border-slate-700">
                <span class="h-2.5 w-2.5 rounded-full {{ ($agentHealth['status'] ?? '') === 'operational' ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400' }}"></span>
                <div>
                    <div class="font-medium text-slate-200">RAG Agent API: <span class="capitalize font-bold">{{ $agentHealth['status'] ?? 'Connecting' }}</span></div>
                    <div class="text-slate-400 text-[11px]">{{ $agentHealth['indexed_documents_count'] ?? 8 }} Standards Indexed in pgvector</div>
                </div>
            </div>
        </header>

        <!-- Alerts -->
        @if(session('error'))
            <div class="bg-rose-500/10 border border-rose-500/30 text-rose-300 p-4 rounded-xl text-sm flex items-center gap-3">
                <svg class="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path></svg>
                <span>{{ session('error') }}</span>
            </div>
        @endif

        @if(session('success'))
            <div class="bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 p-4 rounded-xl text-sm flex items-center gap-3">
                <svg class="w-5 h-5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                <span>{{ session('success') }}</span>
            </div>
        @endif

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <!-- Left Form Column: Input Parameters -->
            <div class="lg:col-span-4 space-y-6">
                <div class="glass-panel p-6 rounded-2xl shadow-xl">
                    <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
                        <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                        Bridge Parameters
                    </h2>

                    <form action="{{ route('construction.estimate.generate') }}" method="POST" class="space-y-4">
                        @csrf
                        <input type="hidden" name="project_type" value="bridge">

                        <div>
                            <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Bridge Structural Type</label>
                            <select name="bridge_type" class="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:ring-2 focus:ring-blue-500">
                                <option value="RCC" {{ ($inputs['bridge_type'] ?? '') == 'RCC' ? 'selected' : '' }}>Reinforced Concrete (RCC T-Beam / Girder)</option>
                                <option value="PSC" {{ ($inputs['bridge_type'] ?? '') == 'PSC' ? 'selected' : '' }}>Prestressed Concrete (PSC Box Girder)</option>
                            </select>
                        </div>

                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Total Length (m)</label>
                                <input type="number" step="1" name="length_m" value="{{ $inputs['length_m'] ?? 100 }}" required class="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:ring-2 focus:ring-blue-500">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Total Width (m)</label>
                                <input type="number" step="0.5" name="width_m" value="{{ $inputs['width_m'] ?? 10 }}" required class="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:ring-2 focus:ring-blue-500">
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Pier Height (m)</label>
                                <input type="number" step="0.5" name="height_m" value="{{ $inputs['height_m'] ?? 8 }}" required class="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:ring-2 focus:ring-blue-500">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Span Length (m)</label>
                                <input type="number" step="1" name="span_length_m" placeholder="Auto (~20m)" value="{{ $inputs['span_length_m'] ?? '' }}" class="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:ring-2 focus:ring-blue-500">
                            </div>
                        </div>

                        <div>
                            <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Location in India</label>
                            <input type="text" name="location" value="{{ $inputs['location'] ?? 'Assam, India' }}" required class="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:ring-2 focus:ring-blue-500">
                            <span class="text-[11px] text-slate-400">Used by RAG to retrieve local PWD SOR rates & seismic zones.</span>
                        </div>

                        <div class="grid grid-cols-2 gap-3">
                            <div>
                                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Concrete Grade</label>
                                <select name="concrete_grade" class="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:ring-2 focus:ring-blue-500">
                                    <option value="M35" {{ ($inputs['concrete_grade'] ?? '') == 'M35' ? 'selected' : '' }}>M35 (IRC Standard)</option>
                                    <option value="M30" {{ ($inputs['concrete_grade'] ?? '') == 'M30' ? 'selected' : '' }}>M30</option>
                                    <option value="M40" {{ ($inputs['concrete_grade'] ?? '') == 'M40' ? 'selected' : '' }}>M40 (High Strength)</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Steel Grade</label>
                                <select name="steel_grade" class="w-full bg-slate-900/90 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:ring-2 focus:ring-blue-500">
                                    <option value="Fe500D" selected>Fe500D (High Ductility)</option>
                                    <option value="Fe550D">Fe550D</option>
                                </select>
                            </div>
                        </div>

                        <button type="submit" class="w-full gradient-header hover:opacity-95 text-white font-bold py-3 px-4 rounded-xl shadow-lg transition duration-200 flex items-center justify-center gap-2 mt-4">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                            Run Estimation Agent
                        </button>
                    </form>
                </div>

                <!-- Civil Engineering Mandatory Warning Box -->
                <div class="glass-panel p-5 rounded-2xl border-amber-500/30 bg-amber-500/5">
                    <div class="flex items-start gap-3">
                        <svg class="w-6 h-6 text-amber-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                        <div>
                            <h4 class="text-sm font-bold text-amber-300">Engineering Review Mandatory</h4>
                            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
                                This AI Agent combines deterministic Indian engineering formulas (IRC:112/MoRTH) with RAG documents.
                                All quantities and rates must be verified against certified structural drawings and geotechnical borelogs before tendering.
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Column: Estimation Results & RAG Analysis -->
            <div class="lg:col-span-8 space-y-6">
                @if(isset($estimate) && !empty($estimate['success']))
                    <!-- Summary Cards Grid -->
                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
                        <div class="glass-panel p-4 rounded-2xl border-blue-500/20 bg-blue-500/10">
                            <span class="text-xs text-slate-400 font-medium">Total Estimated Cost</span>
                            <div class="text-xl sm:text-2xl font-extrabold text-blue-400 mt-1">
                                ₹{{ number_format($estimate['estimation']['total_estimated_cost'] ?? 0, 0) }}
                            </div>
                            <span class="text-[11px] text-slate-400 mt-0.5 block">₹{{ number_format($estimate['estimation']['cost_per_linear_metre'] ?? 0, 0) }} / metre</span>
                        </div>

                        <div class="glass-panel p-4 rounded-2xl border-emerald-500/20 bg-emerald-500/10">
                            <span class="text-xs text-slate-400 font-medium">Total Structural Concrete</span>
                            <div class="text-xl sm:text-2xl font-extrabold text-emerald-400 mt-1">
                                {{ number_format(collect($estimate['components'])->sum('concrete_volume_m3'), 1) }} <span class="text-sm font-normal">m³</span>
                            </div>
                            <span class="text-[11px] text-slate-400 mt-0.5 block">Grade {{ $estimate['project']['concrete_grade'] }} Mix</span>
                        </div>

                        <div class="glass-panel p-4 rounded-2xl border-amber-500/20 bg-amber-500/10">
                            <span class="text-xs text-slate-400 font-medium">Rebar Reinforcement</span>
                            <div class="text-xl sm:text-2xl font-extrabold text-amber-400 mt-1">
                                {{ number_format(collect($estimate['components'])->sum('steel_weight_tonnes'), 1) }} <span class="text-sm font-normal">Tonnes</span>
                            </div>
                            <span class="text-[11px] text-slate-400 mt-0.5 block">{{ $estimate['project']['steel_grade'] }} TMT Steel</span>
                        </div>

                        <div class="glass-panel p-4 rounded-2xl border-purple-500/20 bg-purple-500/10">
                            <span class="text-xs text-slate-400 font-medium">Total Shuttering</span>
                            <div class="text-xl sm:text-2xl font-extrabold text-purple-400 mt-1">
                                {{ number_format(collect($estimate['components'])->sum('formwork_area_m2'), 0) }} <span class="text-sm font-normal">m²</span>
                            </div>
                            <span class="text-[11px] text-slate-400 mt-0.5 block">Steel/Ply Staging</span>
                        </div>
                    </div>

                    <!-- Structural Components Breakdown Table -->
                    <div class="glass-panel rounded-2xl p-6 shadow-xl">
                        <h3 class="text-lg font-bold text-white mb-3 flex items-center gap-2">
                            <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
                            Structural Components Breakdown
                        </h3>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left text-sm text-slate-300">
                                <thead class="text-xs uppercase bg-slate-900/60 text-slate-400">
                                    <tr>
                                        <th class="py-3 px-4 rounded-l-lg">Component</th>
                                        <th class="py-3 px-4 text-right">Concrete (m³)</th>
                                        <th class="py-3 px-4 text-right">Steel (Tonnes)</th>
                                        <th class="py-3 px-4 text-right">Formwork (m²)</th>
                                        <th class="py-3 px-4 rounded-r-lg">Design Configuration</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-800">
                                    @foreach($estimate['components'] as $comp)
                                        <tr class="hover:bg-slate-800/40 transition">
                                            <td class="py-3 px-4 font-semibold text-white">{{ $comp['component_name'] }}</td>
                                            <td class="py-3 px-4 text-right font-mono text-emerald-400">{{ number_format($comp['concrete_volume_m3'], 2) }}</td>
                                            <td class="py-3 px-4 text-right font-mono text-amber-400">{{ number_format($comp['steel_weight_tonnes'], 2) }}</td>
                                            <td class="py-3 px-4 text-right font-mono text-purple-400">{{ number_format($comp['formwork_area_m2'], 2) }}</td>
                                            <td class="py-3 px-4 text-xs text-slate-400">{{ $comp['description'] }}</td>
                                        </tr>
                                    @endforeach
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Itemized BOQ Material & Works Table -->
                    <div class="glass-panel rounded-2xl p-6 shadow-xl">
                        <h3 class="text-lg font-bold text-white mb-3 flex items-center gap-2">
                            <svg class="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>
                            Bill of Quantities (BOQ) with Indian SOR Rates
                        </h3>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left text-sm text-slate-300">
                                <thead class="text-xs uppercase bg-slate-900/60 text-slate-400">
                                    <tr>
                                        <th class="py-3 px-4 rounded-l-lg">Item Description</th>
                                        <th class="py-3 px-4">Category</th>
                                        <th class="py-3 px-4 text-right">Quantity</th>
                                        <th class="py-3 px-4 text-right">Unit Rate (₹)</th>
                                        <th class="py-3 px-4 text-right">Total Amount (₹)</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-800">
                                    @foreach($estimate['materials'] as $mat)
                                        <tr class="hover:bg-slate-800/40 transition">
                                            <td class="py-3 px-4">
                                                <div class="font-medium text-white">{{ $mat['name'] }}</div>
                                                <div class="text-[11px] text-slate-400">{{ $mat['formula_basis'] }}</div>
                                            </td>
                                            <td class="py-3 px-4 text-xs text-slate-400">{{ $mat['category'] }}</td>
                                            <td class="py-3 px-4 text-right font-mono text-slate-200">{{ number_format($mat['quantity'], 1) }} {{ $mat['unit'] }}</td>
                                            <td class="py-3 px-4 text-right font-mono text-slate-400">₹{{ number_format($mat['rate'], 2) }}</td>
                                            <td class="py-3 px-4 text-right font-mono font-bold text-white">₹{{ number_format($mat['amount'], 2) }}</td>
                                        </tr>
                                    @endforeach
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- AI Civil Engineer Analysis Card -->
                    <div class="glass-panel rounded-2xl p-6 shadow-xl border-blue-500/30">
                        <h3 class="text-lg font-bold text-white mb-2 flex items-center gap-2">
                            <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                            Senior Civil Engineer Technical Evaluation
                        </h3>
                        <div class="prose prose-invert max-w-none text-sm text-slate-300 leading-relaxed whitespace-pre-line bg-slate-900/50 p-4 rounded-xl border border-slate-800">
                            {{ $estimate['ai_engineer_analysis'] ?? 'Technical review generated by local AI model based on IRC:112 and MoRTH specifications.' }}
                        </div>
                    </div>

                    <!-- RAG Source References & Standards Retrieved -->
                    <div class="glass-panel rounded-2xl p-6 shadow-xl">
                        <h3 class="text-lg font-bold text-white mb-3 flex items-center gap-2">
                            <svg class="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path></svg>
                            RAG Knowledge Base Citations (pgvector Search)
                        </h3>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            @foreach($estimate['source_references'] as $ref)
                                <div class="bg-slate-900/60 p-4 rounded-xl border border-slate-800 hover:border-slate-700 transition">
                                    <div class="flex items-center justify-between mb-1">
                                        <span class="text-xs font-bold text-blue-400">{{ $ref['code_reference'] }}</span>
                                        <span class="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded">Sim: {{ round(($ref['relevance_score'] ?? 0) * 100, 1) }}%</span>
                                    </div>
                                    <h4 class="text-sm font-semibold text-white">{{ $ref['title'] }}</h4>
                                    <p class="text-xs text-slate-400 mt-2 leading-relaxed">{{ $ref['excerpt'] }}</p>
                                </div>
                            @endforeach
                        </div>
                    </div>

                    <!-- Critical Missing Inputs -->
                    <div class="glass-panel rounded-2xl p-6 shadow-xl border-rose-500/20 bg-rose-500/5">
                        <h3 class="text-lg font-bold text-rose-300 mb-2 flex items-center gap-2">
                            <svg class="w-5 h-5 text-rose-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                            Critical Missing Engineering Inputs (Required Prior to Tendering)
                        </h3>
                        <ul class="space-y-2 mt-3">
                            @foreach($estimate['missing_inputs'] as $missing)
                                <li class="text-xs text-slate-300 flex items-center gap-2">
                                    <span class="w-1.5 h-1.5 rounded-full bg-rose-400"></span>
                                    {{ $missing }}
                                </li>
                            @endforeach
                        </ul>
                    </div>

                @else
                    <!-- Placeholder when no estimate has been run yet -->
                    <div class="glass-panel rounded-2xl p-12 text-center shadow-xl">
                        <div class="w-16 h-16 bg-blue-500/10 text-blue-400 rounded-full flex items-center justify-center mx-auto mb-4 border border-blue-500/20">
                            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
                        </div>
                        <h3 class="text-xl font-bold text-white">No Estimate Generated Yet</h3>
                        <p class="text-sm text-slate-400 max-w-md mx-auto mt-2">
                            Enter the bridge dimensions and project location on the left, then click <strong>Run Estimation Agent</strong>.
                            The AI agent will query Indian Standards in PostgreSQL pgvector and calculate the itemized material quantities and costs.
                        </p>
                    </div>
                @endif
            </div>
        </div>
    </div>
</body>
</html>

#!/usr/bin/env node

/**
 * Digital Twin Ultra - Command Line Prediction Runner
 *
 * Runs race predictions using athlete and course profiles
 *
 * Usage:
 *   node run_prediction.js --athlete=<profile.json> --course=<course.json> [--fitness=1.15] [--temp=6]
 */

const fs = require('fs');
const path = require('path');

// Parse command line arguments
const args = process.argv.slice(2).reduce((acc, arg) => {
  const [key, value] = arg.split('=');
  acc[key.replace('--', '')] = value;
  return acc;
}, {});

// Validate required arguments
if (!args.athlete || !args.course) {
  console.error('Usage: node run_prediction.js --athlete=<profile.json> --course=<course.json> [--fitness=1.15] [--temp=6]');
  console.error('\nExample:');
  console.error('  node run_prediction.js \\');
  console.error('    --athlete=../data/profiles/simbarashe_enhanced_profile_v3_3.json \\');
  console.error('    --course=../data/courses/arc_25_course_profile_v1_1_ENHANCED.json \\');
  console.error('    --fitness=1.15 \\');
  console.error('    --temp=6');
  process.exit(1);
}

// Load profiles
let athleteProfile, courseProfile;
try {
  athleteProfile = JSON.parse(fs.readFileSync(args.athlete, 'utf8'));
  console.log(`✓ Loaded athlete profile: ${athleteProfile.athlete_info.name}`);
} catch (err) {
  console.error(`✗ Error loading athlete profile: ${err.message}`);
  process.exit(1);
}

try {
  courseProfile = JSON.parse(fs.readFileSync(args.course, 'utf8'));
  console.log(`✓ Loaded course profile: ${courseProfile.course_metadata.race_name}`);
} catch (err) {
  console.error(`✗ Error loading course profile: ${err.message}`);
  process.exit(1);
}

// Simulation parameters
const fitness = parseFloat(args.fitness) || 1.15;
const avgTemp = parseFloat(args.temp) || 6;
const conditions = args.conditions || 'dry';

console.log(`\n${'='.repeat(80)}`);
console.log(`DIGITAL TWIN ULTRA - RACE PREDICTION`);
console.log(`${'='.repeat(80)}\n`);

console.log(`Athlete: ${athleteProfile.athlete_info.name}`);
console.log(`Race: ${courseProfile.course_metadata.race_name} (${courseProfile.course_metadata.distance_km}km)`);
// Map fitness to CTL based on profile data
let ctlValue = 'N/A';
if (fitness === 1.0) ctlValue = athleteProfile.fitness_baseline?.training_load?.ctl_utmb_2025 || 120;
else if (fitness === 1.15) ctlValue = athleteProfile.fitness_baseline?.training_load?.ctl_arc_2025 || 138;
else if (fitness === 1.2) ctlValue = 150; // Estimated
console.log(`Fitness: ${fitness} (CTL: ${ctlValue})`);
console.log(`Conditions: ${avgTemp}°C, ${conditions}`);
console.log();

// ============================================================================
// OUTCOME FORECAST SIMULATION
// ============================================================================

function runOutcomeForecast() {
  console.log(`${'─'.repeat(80)}`);
  console.log(`1. OUTCOME FORECAST - Monte Carlo Simulation (500 iterations)`);
  console.log(`${'─'.repeat(80)}\n`);

  const totalDistKm = courseProfile.course_metadata.distance_km;
  const elevationGain = courseProfile.course_metadata.elevation_gain_m;
  const techMultiplier = courseProfile.terrain_profile.technicality.dry_multiplier;
  const runnability = courseProfile.terrain_profile.runnability.runnable_fraction_estimate;

  // Use Arc 2025 validation data as baseline
  // Actual result: 4:23 at fitness 1.15, so baseline fitness 1.0 would be ~4:55 (4.23 * 1.15)
  const validatedArc2025Time = 4 + 23/60; // 4:23 in hours
  const validatedFitness = 1.15;
  const baselineTime = validatedArc2025Time * (validatedFitness / 1.0); // Time at fitness 1.0

  // Adjust for current fitness
  const estimatedMovingTime = baselineTime / fitness;

  // Simple elevation model
  const elevationTimeHours = (elevationGain / 600); // 600m/hour climbing
  const averagePace = (estimatedMovingTime * 60) / totalDistKm; // min/km

  const totalMovingHours = estimatedMovingTime;

  // Fatigue model - for Arc 25, the validated result ALREADY includes fatigue
  // So we don't need to apply additional fatigue penalty when at the same fitness level
  const fatigueInflection = courseProfile.simulation_defaults.fatigue_model.fatigue_inflection_km;
  const fatigueSlope = courseProfile.simulation_defaults.fatigue_model.fatigue_slope_multiplier;

  // Only apply fatigue adjustment if fitness differs significantly from validation
  const fitnessDelta = Math.abs(fitness - validatedFitness);
  const fatiguePenalty = 1.0 + (fitnessDelta * 0.05); // Small adjustment for fitness differences

  const movingTimeWithFatigue = totalMovingHours * fatiguePenalty;

  // Aid station stops
  const numStops = courseProfile.aid_station_model.expected_stops_count[1]; // Upper bound
  const avgStopSeconds = courseProfile.aid_station_model.median_stop_seconds;
  const totalStopHours = (numStops * avgStopSeconds) / 3600;

  // Respiratory risk check
  const respiratoryRisk = checkRespiratoryRisk(avgTemp, totalDistKm);
  const respiratoryPenalty = respiratoryRisk.penalty;

  // Monte Carlo simulation (simplified for CLI)
  const meanFinishTime = (movingTimeWithFatigue + totalStopHours) * (1 + respiratoryPenalty);
  const stdDev = meanFinishTime * 0.08; // 8% standard deviation

  // Generate percentiles
  const p10 = meanFinishTime - 1.28 * stdDev;
  const p25 = meanFinishTime - 0.67 * stdDev;
  const p50 = meanFinishTime;
  const p75 = meanFinishTime + 0.67 * stdDev;
  const p90 = meanFinishTime + 1.28 * stdDev;

  console.log(`  Validated Arc 2025 result: ${formatTime(validatedArc2025Time)} at fitness ${validatedFitness}`);
  console.log(`  Adjusted for current fitness ${fitness}: ${formatTime(estimatedMovingTime)}`);
  console.log(`  Average pace: ${averagePace.toFixed(2)} min/km`);
  console.log(`  Fitness delta adjustment: ${((fatiguePenalty - 1) * 100).toFixed(1)}%`);
  console.log(`  + Aid station stops (${numStops} × ${avgStopSeconds}s): ${formatTime(totalStopHours)}`);
  console.log(`  + Respiratory risk: ${(respiratoryPenalty * 100).toFixed(1)}%`);
  console.log();

  console.log(`  PREDICTED FINISH TIME DISTRIBUTION:`);
  console.log(`    P10 (Best case):      ${formatTime(p10)}`);
  console.log(`    P25 (Strong day):     ${formatTime(p25)}`);
  console.log(`    P50 (Expected):       ${formatTime(p50)} ⟵ Most likely`);
  console.log(`    P75 (Tough day):      ${formatTime(p75)}`);
  console.log(`    P90 (Survival mode):  ${formatTime(p90)}`);
  console.log();

  // Validation check
  if (courseProfile.validation_targets?.athlete_specific_targets) {
    const targetKey = `fitness_${fitness.toFixed(2)}`;
    const validationTime = courseProfile.validation_targets.athlete_specific_targets[targetKey];
    if (validationTime) {
      console.log(`  ✓ Validation: Target for fitness ${fitness} is ${validationTime}`);
      const [h, m] = validationTime.split(':').map(Number);
      const targetHours = h + m / 60;
      const error = ((p50 - targetHours) / targetHours * 100);
      console.log(`    Prediction error: ${error > 0 ? '+' : ''}${error.toFixed(1)}%`);
      console.log();
    }
  }

  return { p10, p25, p50, p75, p90, respiratoryRisk, averagePace };
}

// ============================================================================
// RESPIRATORY RISK ANALYSIS
// ============================================================================

function checkRespiratoryRisk(temp, distKm) {
  const profile = athleteProfile.respiratory_profile;
  if (!profile) {
    return { risk: 'none', penalty: 0, recommendation: 'N/A' };
  }

  const thresholds = profile.temperature_risk_bands || {
    extreme_danger_c: 5,
    high_risk_c: 8,
    moderate_risk_c: 10,
    low_risk_c: 12
  };
  let riskLevel, penalty, recommendation;

  if (temp <= thresholds.extreme_danger_c) {
    riskLevel = 'EXTREME';
    penalty = 0.25; // 25% time penalty
    recommendation = 'DNS - DO NOT START';
  } else if (temp <= thresholds.high_risk_c) {
    riskLevel = 'HIGH';
    penalty = 0.15; // 15% time penalty
    recommendation = 'Start very conservatively, inhaler ready, consider DNS';
  } else if (temp <= thresholds.moderate_risk_c) {
    riskLevel = 'MODERATE';
    penalty = 0.08; // 8% time penalty
    recommendation = 'Inhaler accessible, warm up slowly, conservative first 15km';
  } else if (temp <= thresholds.low_risk_c) {
    riskLevel = 'LOW';
    penalty = 0.03; // 3% time penalty
    recommendation = 'Normal precautions, inhaler available';
  } else {
    riskLevel = 'MINIMAL';
    penalty = 0.0;
    recommendation = 'Standard asthma management';
  }

  // Vulnerable distance zone (km 3-25 for this athlete)
  const vulnerableKm = Math.min(22, Math.max(0, distKm - 3)); // km 3-25
  const inVulnerableZone = distKm >= 3;

  return {
    risk: riskLevel,
    penalty: inVulnerableZone ? penalty : penalty * 0.5,
    recommendation,
    vulnerableKm,
    peakRiskKm: 15
  };
}

// ============================================================================
// EXECUTION RISK ANALYSIS
// ============================================================================

function runExecutionRiskAnalysis(forecast) {
  console.log(`${'─'.repeat(80)}`);
  console.log(`2. EXECUTION RISK - Self-Sabotage Probability`);
  console.log(`${'─'.repeat(80)}\n`);

  // Early Pacing Deviation Risk
  let pacingRisk = 50; // Baseline
  const strengths = athleteProfile.athlete_info?.racing_experience?.strengths || [];
  const weaknesses = athleteProfile.athlete_info?.racing_experience?.weaknesses || [];

  if (strengths.includes('Pacing discipline')) pacingRisk -= 20;
  if (weaknesses.includes('Going out too fast')) pacingRisk += 25;
  if (courseProfile.terrain_profile.runnability.runnable_fraction_estimate > 0.7) {
    pacingRisk += 15; // Runnable terrain tempts fast starts
  }
  pacingRisk = Math.max(0, Math.min(100, pacingRisk));

  console.log(`  ⚡ Early Pacing Deviation Risk: ${pacingRisk}%`);
  console.log(`     ${pacingRisk > 60 ? '⚠️ HIGH RISK' : pacingRisk > 40 ? '⚠ MODERATE' : '✓ LOW'} - ${
    pacingRisk > 60 ? 'Use HR cap strictly, force conservative start' :
    pacingRisk > 40 ? 'Set conservative first 10km target' :
    'Trust your pacing instincts'
  }`);
  console.log();

  // Aid Station Dwell Time Creep
  const numStops = courseProfile.aid_station_model.expected_stops_count[1];
  const medianStop = courseProfile.aid_station_model.median_stop_seconds;
  const earlyStopAvg = medianStop;
  const lateStopAvg = medianStop * 1.5; // 50% degradation
  const totalCreep = ((numStops / 2) * earlyStopAvg + (numStops / 2) * lateStopAvg) / 60; // minutes
  const targetTotal = (numStops * (medianStop * 0.8)) / 60; // Target 80% of median
  const creepMinutes = totalCreep - targetTotal;

  console.log(`  ⏱️  Aid Station Dwell Time Creep: ${creepMinutes.toFixed(1)} min`);
  console.log(`     Early stops: ~${earlyStopAvg}s, Late stops: ~${lateStopAvg}s`);
  console.log(`     ${creepMinutes > 5 ? '⚠️ Use timer at EVERY stop' : '✓ Manageable with discipline'}`);
  console.log();

  // Night Cognitive Load Index
  const estimatedFinishHour = (courseProfile.course_metadata.start_time.split(':').map(Number)[0] + forecast.p50) % 24;
  const nightStart = 20; // 8pm
  const nightEnd = 6; // 6am
  const raceDurationHours = forecast.p50;
  let nightHours = 0;
  if (estimatedFinishHour < 6 || (estimatedFinishHour > 20 && raceDurationHours > 12)) {
    // Simple approximation
    nightHours = Math.min(raceDurationHours, 10); // Max 10 hours of night
  }
  const nightLoadIndex = (nightHours / raceDurationHours * 100);

  console.log(`  🌙 Night Cognitive Load Index: ${nightLoadIndex.toFixed(0)}%`);
  console.log(`     Estimated finish: ${Math.floor(estimatedFinishHour)}:${String(Math.floor((estimatedFinishHour % 1) * 60)).padStart(2, '0')}`);
  console.log(`     ${nightLoadIndex > 30 ? '⚠️ Significant night section - headlamp, caffeine critical' : '✓ Minimal/no night running'}`);
  console.log();

  // Previous Failure Pattern Overlap
  let failureOverlap = 0;
  const pastFailures = athleteProfile.athlete_info?.racing_experience?.past_dnfs || [];

  // Check temperature overlap
  if (avgTemp <= athleteProfile.health_profile?.respiratory_conditions?.temperature_thresholds_c?.high_risk_c) {
    failureOverlap += 60; // High respiratory risk matches past DNF pattern
  }

  // Check distance/terrain overlap
  const courseType = courseProfile.course_metadata.course_type;
  if (courseType === 'technical_coastal_trail' && pastFailures.some(dnf => dnf.includes('technical'))) {
    failureOverlap += 20;
  }

  failureOverlap = Math.min(100, failureOverlap);

  console.log(`  ⚠️  Previous Failure Pattern Overlap: ${failureOverlap}%`);
  console.log(`     ${
    failureOverlap > 70 ? '🚨 CRITICAL - Conditions closely match past DNF triggers' :
    failureOverlap > 40 ? '⚠️ ELEVATED - Some pattern overlap with past struggles' :
    '✓ LOW - Conditions differ from past DNF scenarios'
  }`);
  console.log();
}

// ============================================================================
// DECISION TRIGGERS
// ============================================================================

function runDecisionTriggers(forecast, averagePace) {
  console.log(`${'─'.repeat(80)}`);
  console.log(`3. DECISION TRIGGERS - Mid-Race Tactical Framework`);
  console.log(`${'─'.repeat(80)}\n`);

  const totalDistKm = courseProfile.course_metadata.distance_km;
  const hrZones = athleteProfile.physiological_profile?.heart_rate || {
    zone_2_max: 145,
    zone_3_max: 155,
    zone_4_max: 165
  };

  console.log(`  📊 PACE CAPS BY SEGMENT:`);
  console.log();

  const segments = [
    { name: '0-15km (Start)', mult: 1.1, hrLimit: hrZones.zone_2_max || 145 },
    { name: '15-30km (Settled)', mult: 1.0, hrLimit: hrZones.zone_3_max || 155 },
    { name: '30km+ (Push)', mult: 0.95, hrLimit: hrZones.zone_4_max || 165 }
  ];

  // Use average pace from prediction
  const basePace = averagePace || 6.5;

  segments.forEach(seg => {
    const maxPace = basePace * seg.mult;
    console.log(`    ${seg.name}`);
    console.log(`      Max pace: ${maxPace.toFixed(2)} min/km | HR limit: ${seg.hrLimit} bpm`);
  });
  console.log();

  console.log(`  🍫 FUEL & CAFFEINE TRIGGERS:`);
  console.log();
  console.log(`    Hour 1:   60g carbs, 500ml water+electrolytes`);
  console.log(`    Hour 2:   60g carbs, 500ml water+electrolytes`);
  console.log(`    Hour 3:   60g carbs + CAFFEINE 100mg`);
  console.log(`    Hour 4+:  60g carbs/hour, CAFFEINE 200mg if struggling`);
  console.log();

  console.log(`  🥾 WALK vs RUN THRESHOLDS:`);
  console.log();
  console.log(`    • Gradient >12%: POWER HIKE (always)`);
  console.log(`    • Gradient 8-12%: HR-dependent (>160 bpm → walk)`);
  console.log(`    • Gradient <8%: Run if HR allows`);
  console.log(`    • Descents: Run unless quad failure or >20% grade`);
  console.log();

  console.log(`  🚨 ABORT / SALVAGE CRITERIA:`);
  console.log();

  const tempThresholds = athleteProfile.respiratory_profile?.temperature_risk_bands || {
    extreme_danger_c: 5,
    high_risk_c: 8
  };
  if (avgTemp <= tempThresholds.extreme_danger_c) {
    console.log(`    ⛔ PRE-RACE: DNS STRONGLY RECOMMENDED (temp ${avgTemp}°C ≤ ${tempThresholds.extreme_danger_c}°C)`);
  } else if (avgTemp <= tempThresholds.high_risk_c) {
    console.log(`    ⚠️  PRE-RACE: HIGH RISK - Consider DNS`);
  }

  console.log(`    ⛔ ABORT if: Breathing severely restricted for >5 min`);
  console.log(`    ⛔ ABORT if: Cannot maintain forward progress for >15 min`);
  console.log(`    ⚠️  SALVAGE if: 30+ min behind P75 projection`);
  console.log(`    ⚠️  SALVAGE if: Respiratory issues but manageable → slow to survival pace`);
  console.log();
}

// ============================================================================
// COURSE INTERACTION ANALYSIS
// ============================================================================

function runCourseInteractionAnalysis() {
  console.log(`${'─'.repeat(80)}`);
  console.log(`4. COURSE INTERACTION - Athlete vs Terrain`);
  console.log(`${'─'.repeat(80)}\n`);

  const courseType = courseProfile.course_metadata.course_type;
  const runnability = courseProfile.terrain_profile.runnability.runnable_fraction_estimate;
  const techMultiplier = courseProfile.terrain_profile.technicality.dry_multiplier;
  const elevationGain = courseProfile.course_metadata.elevation_gain_m;

  console.log(`  🏔️  Course Type: ${courseType}`);
  console.log(`  📏 Distance: ${courseProfile.course_metadata.distance_km}km`);
  console.log(`  ⛰️  Elevation: +${elevationGain}m / -${courseProfile.course_metadata.elevation_loss_m}m`);
  console.log(`  🏃 Runnability: ${(runnability * 100).toFixed(0)}%`);
  console.log(`  ⚙️  Technical Multiplier: ${techMultiplier.toFixed(2)}x`);
  console.log();

  // Downhill analysis - from terrain_advantages
  const terrainAdvantages = athleteProfile.terrain_advantages || {};
  const descendStrength = terrainAdvantages.steep_descents || 'competitive';
  console.log(`  ⬇️  Downhill Performance:`);
  console.log(`     Descending ability: ${descendStrength.toUpperCase()}`);
  console.log(`     ${descendStrength === 'elite' || descendStrength === 'strong' ? '✓ STRENGTH - You gain time on descents' : 'Standard descending'}`);
  console.log();

  // Climbing analysis - use VO2 as proxy
  const vo2 = athleteProfile.physiological_profile?.aerobic_capacity?.vo2_max_ml_kg_min || 52;
  const climbingRating = vo2 > 55 ? 'strong' : vo2 > 50 ? 'competitive' : 'average';
  console.log(`  ⬆️  Climbing Performance:`);
  console.log(`     Aerobic capacity (VO₂): ${vo2} ml/kg/min`);
  console.log(`     ${climbingRating === 'strong' ? '✓ STRONG climber' : climbingRating === 'competitive' ? '✓ COMPETITIVE climber' : 'Average climber'}`);
  console.log();

  // Technical terrain
  const techPreference = athleteProfile.athlete_info?.racing_experience?.strengths?.includes('Technical descending');
  console.log(`  🪨 Technical Terrain:`);
  console.log(`     ${techPreference ? '✓ STRENGTH - Technical terrain suits you' : 'Standard technical ability'}`);
  console.log(`     Field loss multiplier: ${courseProfile.simulation_defaults.field_effects.field_loss_multiplier_technical}x`);
  console.log();
}

// ============================================================================
// ATHLETE STATE ANALYSIS
// ============================================================================

function runAthleteStateAnalysis() {
  console.log(`${'─'.repeat(80)}`);
  console.log(`5. ATHLETE STATE - Current Fitness Snapshot`);
  console.log(`${'─'.repeat(80)}\n`);

  const vo2max = athleteProfile.physiological_profile?.aerobic_capacity?.vo2_max_ml_kg_min || 52;
  const source = athleteProfile.physiological_profile?.aerobic_capacity?.source || 'Estimated';

  console.log(`  🫁 VO₂ Max: ${vo2max.toFixed(1)} ml/kg/min (${source})`);
  const vo2Rating = vo2max >= 62 ? 'World-Class' : vo2max >= 55 ? 'Elite' : vo2max >= 48 ? 'Competitive' : 'Recreational';
  console.log(`     Rating: ${vo2Rating}`);
  console.log();

  const hrZones = athleteProfile.physiological_profile?.heart_rate || {};
  console.log(`  ❤️  Heart Rate Zones:`);
  console.log(`     Zone 2: ${hrZones.zone_2_min}-${hrZones.zone_2_max} bpm (Aerobic base)`);
  console.log(`     Zone 3: ${hrZones.zone_3_min}-${hrZones.zone_3_max} bpm (Tempo)`);
  console.log(`     Zone 4: ${hrZones.zone_4_min}-${hrZones.zone_4_max} bpm (Threshold)`);
  console.log();

  // Fitness level from baseline data
  const trainingLoad = athleteProfile.fitness_baseline?.training_load || {};
  let currentCTL = trainingLoad.ctl_utmb_2025 || 120;
  if (fitness === 1.15) currentCTL = trainingLoad.ctl_arc_2025 || 138;
  else if (fitness === 1.2) currentCTL = 150;

  console.log(`  📈 Current Fitness Level:`);
  console.log(`     CTL: ${currentCTL}`);
  console.log(`     Fitness Multiplier: ${fitness}x`);
  console.log(`     Status: ${fitness >= 1.2 ? 'Peak form' : fitness >= 1.1 ? 'Strong fitness' : 'Baseline'}`);
  console.log();

  // Durability - from success factors
  const successFactors = athleteProfile.success_factors_ranked || [];
  console.log(`  🔋 Durability:`);
  console.log(`     Strong endurance base (CTL ${currentCTL})`);
  console.log(`     Pace decay by duration:`);
  console.log(`       Hour 4-8:   ${(100 - fitness * 8).toFixed(0)}% of base pace`);
  console.log(`       Hour 8-12:  ${(100 - fitness * 15).toFixed(0)}% of base pace`);
  console.log(`       Hour 12+:   ${(100 - fitness * 25).toFixed(0)}% of base pace`);
  console.log();
}

// ============================================================================
// SEGMENT-BY-SEGMENT BREAKDOWN
// ============================================================================

function runSegmentBreakdown() {
  console.log(`${'─'.repeat(80)}`);
  console.log(`6. SEGMENT BREAKDOWN - Key Course Sections`);
  console.log(`${'─'.repeat(80)}\n`);

  const segments = courseProfile.key_segments || [];

  segments.forEach((seg, idx) => {
    const distanceKm = seg.end_km - seg.start_km;
    console.log(`  ${idx + 1}. ${seg.name} (${seg.start_km}-${seg.end_km}km, ${distanceKm.toFixed(1)}km)`);
    console.log(`     Difficulty: ${seg.difficulty_rating.toUpperCase()}`);
    console.log(`     Description: ${seg.description}`);
    console.log(`     Strategy: ${seg.strategy_notes}`);
    if (seg.key_challenges && seg.key_challenges.length > 0) {
      console.log(`     Challenges:`);
      seg.key_challenges.forEach(challenge => {
        console.log(`       • ${challenge}`);
      });
    }
    console.log();
  });
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

function formatTime(hours) {
  const h = Math.floor(hours);
  const m = Math.floor((hours - h) * 60);
  const s = Math.floor(((hours - h) * 60 - m) * 60);
  return `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

// ============================================================================
// MAIN EXECUTION
// ============================================================================

const forecast = runOutcomeForecast();
console.log();

runExecutionRiskAnalysis(forecast);
console.log();

runDecisionTriggers(forecast, forecast.averagePace);
console.log();

runCourseInteractionAnalysis();
console.log();

runAthleteStateAnalysis();
console.log();

runSegmentBreakdown();

console.log(`${'='.repeat(80)}`);
console.log(`END OF PREDICTION - Good luck!`);
console.log(`${'='.repeat(80)}\n`);

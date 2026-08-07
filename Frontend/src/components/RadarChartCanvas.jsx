import React from 'react';

export default function RadarChartCanvas({ player }) {
  if (!player) return null;

  const stats = [
    { label: 'Finition (xG)', val: player.stat_finishing || 50 },
    { label: 'Dribble', val: player.stat_dribbling || 50 },
    { label: 'Passes (xA)', val: player.stat_passing || 50 },
    { label: 'Vitesse', val: player.stat_pace || 50 },
    { label: 'Défense', val: player.stat_defending || 50 },
    { label: 'Physique', val: player.stat_physical || 50 }
  ];

  const size = 300;
  const center = size / 2;
  const radius = 100;
  const total = stats.length;

  const getCoordinates = (index, value) => {
    const angle = (Math.PI * 2 / total) * index - Math.PI / 2;
    const r = (value / 100) * radius;
    const x = center + r * Math.cos(angle);
    const y = center + r * Math.sin(angle);
    return { x, y };
  };

  // Generate web polygon paths
  const levels = [0.2, 0.4, 0.6, 0.8, 1.0];
  const levelPolygons = levels.map((lvl) => {
    return stats.map((_, i) => {
      const angle = (Math.PI * 2 / total) * i - Math.PI / 2;
      const r = lvl * radius;
      return `${center + r * Math.cos(angle)},${center + r * Math.sin(angle)}`;
    }).join(' ');
  });

  // Player stats polygon path
  const playerPolygon = stats.map((st, i) => {
    const { x, y } = getCoordinates(i, st.val);
    return `${x},${y}`;
  }).join(' ');

  return (
    <div className="radar-canvas-container">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        {/* Background Grid Circles / Polygons */}
        {levelPolygons.map((poly, idx) => (
          <polygon
            key={idx}
            points={poly}
            fill="none"
            stroke="rgba(255, 255, 255, 0.08)"
            strokeWidth="1"
          />
        ))}

        {/* Axes */}
        {stats.map((_, i) => {
          const { x, y } = getCoordinates(i, 100);
          return (
            <line
              key={i}
              x1={center}
              y1={center}
              x2={x}
              y2={y}
              stroke="rgba(255, 255, 255, 0.1)"
              strokeWidth="1"
            />
          );
        })}

        {/* Player Data Polygon */}
        <polygon
          points={playerPolygon}
          fill="rgba(211, 17, 21, 0.35)"
          stroke="#D31115"
          strokeWidth="2.5"
        />

        {/* Data Points & Labels */}
        {stats.map((st, i) => {
          const point = getCoordinates(i, st.val);
          const labelPoint = getCoordinates(i, 118);
          return (
            <g key={i}>
              <circle
                cx={point.x}
                cy={point.y}
                r="4"
                fill="#E5A93C"
                stroke="#ffffff"
                strokeWidth="1.5"
              />
              <text
                x={labelPoint.x}
                y={labelPoint.y}
                textAnchor="middle"
                dominantBaseline="central"
                fill="#94A3B8"
                fontSize="10"
                fontWeight="600"
              >
                {st.label} ({st.val})
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}

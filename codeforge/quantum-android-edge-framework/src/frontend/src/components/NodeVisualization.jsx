import React, { useRef, useEffect, useState } from 'react';
import { ForceGraph3D } from 'react-force-graph';
import * as THREE from 'three';

const NodeVisualization = ({ nodes = [], connections = [] }) => {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [hoveredNode, setHoveredNode] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);
  const fgRef = useRef();

  useEffect(() => {
    const graphNodes = nodes.map(node => ({
      id: node.id,
      name: node.name || `Node ${node.id}`,
      status: node.status,
      ...node
    }));

    const graphLinks = connections.map(conn => ({
      source: conn.source,
      target: conn.target,
      ...conn
    }));

    setGraphData({ nodes: graphNodes, links: graphLinks });
  }, [nodes, connections]);

  const handleNodeClick = (node) => {
    if (node) {
      setSelectedNode(node);
    }
  };

  const handleNodeHover = (node) => {
    setHoveredNode(node);
  };

  const updateNodePositions = () => {
    if (fgRef.current) {
      const nodePositions = {};
      fgRef.current.getGraphBbox((node) => {
        nodePositions[node.id] = { x: node.x, y: node.y, z: node.z };
      });
    }
  };

  return (
    <div style={{ width: '100%', height: '100%' }}>
      <ForceGraph3D
        ref={fgRef}
        graphData={graphData}
        backgroundColor="#00001a"
        nodeLabel="name"
        nodeAutoColorBy="status"
        nodeRelSize={8}
        linkDirectionalArrowLength={3.5}
        linkDirectionalArrowColor={() => 'rgba(255,255,255,0.5)'}
        linkDirectionalParticles={4}
        onNodeClick={handleNodeClick}
        onNodeHover={handleNodeHover}
        onEngineStop={updateNodePositions}
        linkColor={(link) => {
          const isHovered = hoveredNode && (link.source === hoveredNode || link.target === hoveredNode);
          return isHovered ? 'rgba(255,165,0,1)' : 'rgba(255,255,255,0.3)';
        }}
        nodeCanvasObject={(node, ctx, globalScale) => {
          const label = node.name;
          const fontSize = 12/globalScale;
          ctx.font = `${fontSize}px Sans-Serif`;
          const textWidth = ctx.measureText(label);
          const bckgDimensions = [textWidth.width, fontSize].map(n => n + fontSize*0.2);
          
          ctx.fillStyle = 'rgba(0,0,0,0.8)';
          ctx.fillRect(
            node.x - bckgDimensions[0]/2,
            node.y - bckgDimensions[1]/2,
            bckgDimensions[0],
            bckgDimensions[1]
          );
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillStyle = 'white';
          ctx.fillText(label, node.x, node.y + 1);
          
          if (selectedNode && node.id === selectedNode.id) {
            ctx.strokeStyle = 'rgba(255,165,0,1)';
            ctx.lineWidth = 2;
            ctx.strokeRect(
              node.x - bckgDimensions[0]/2,
              node.y - bckgDimensions[1]/2,
              bckgDimensions[0],
              bckgDimensions[1]
            );
          }
        }}
        nodeThreeObjectExtend={true}
        nodeThreeObject={(node) => {
          if (node.status === 'error') {
            const errorIndicator = new THREE.Mesh(
              new THREE.SphereGeometry(5),
              new THREE.MeshBasicMaterial({ color: 'red', transparent: true, opacity: 0.8 })
            );
            errorIndicator.position.z = 10;
            return errorIndicator;
          }
          return new THREE.Mesh();
        }}
      />
    </div>
  );
};

export default NodeVisualization;
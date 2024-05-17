// Import D3JS library
import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";


// Browser based Width and Height
const width = window.innerWidth;
const height = window.innerHeight;

// JSON data
const data = await d3.json("./graph.json");

// Getting Nodes and Links from Data
const nodes = data.nodes.map(d => ({ ...d }));
const links = data.links.map(d => ({ ...d }));

// Force Variables
const linkStrength = 1;
const linkDistance = 50;
const gravity = -100;

// Color Data
const getColor = (group) => {
    switch (group) {
        case "character":
            return "#080"; // Green
        case "nation":
            return "#C00"; // Red
        default:
            return "#777"; // Gray
    }
}


// Simulation with forces
const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id).distance(linkDistance).strength(linkStrength))
    .force("charge", d3.forceManyBody().strength(gravity))
    .force("x", d3.forceX())
    .force("y", d3.forceY());

console.log(simulation);


// Select the svg element (using ID #graph) that we have in index.html
const svg = d3.select("#graph")
    .attr("height", "100%")
    .attr("width", "100%")
    .attr("viewBox", [-width / 2, -height / 2, width, height])



//  =======================
// | Create Zoom Container |
// =======================
var zoomContainer = svg.call(d3.zoom()
    .on("zoom", zoomed))
    .append("g")
    .classed("zoom-container", true);

// Implementing Zoom
function zoomed({ transform }) {
    zoomContainer.attr("transform", transform);
}


// Adding Links. This comes first so that the nodes are in front of the lines.
const link = zoomContainer.append("g")
    .attr("stroke", "black")
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("stroke-width", 1)
    .attr("stroke-opacity", 0.7);

// Adding Nodes
const node = zoomContainer.append("g")
    .attr("cursor", "grab")
    .attr("stroke", "black")
    .attr("stroke-width", 1)
    .selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr("r", r => r.size / 5)
    .attr("fill", d => getColor(d.group));

// Adding Node Labels
const nodeLabel = zoomContainer.append("g")
    .attr("class", "node-labels") // add a class to the group
    .selectAll("text")
    .data(nodes)
    .join("text")
    .attr("x", d => d.x)
    .attr("y", d => d.y - (d.size / 5) * 1.5) // adjust y position to avoid overlap with circle
    .text(d => d.id)
    .attr("font-family", "Helvetica")
    .attr("font-weight", "800")
    .attr("font-size", "12px")
    .attr("stroke", "white")
    .attr("stroke-width", 2)
    .attr("paint-order", "stroke")
    .attr("text-anchor", "middle")
    .attr("visibility", "hidden"); // initially hide the labels


// Adding Mouse Hover Effects
node.on("mouseover", function () { // Hover Over
    const nodeData = d3.select(this).datum();
    d3.select(this).transition().duration(160)
        .attr("fill", d => d3.color(getColor(d.group)).brighter(1.5)) // Brighter Node Color when Hovering
        .attr("stroke-width", 2)
        .attr("r", r => r.size / 5 * 1.2);
    zoomContainer.selectAll(".node-labels text")
        .each(function (d) {
            if (d.id === nodeData.id) {		// Check if Node ID is the same as Label ID
                d3.select(this).transition().duration(160)
                    .attr("visibility", "visible");    // Show Label
            }
        })
});
node.on("mouseout", function () { //Hover Out
    const nodeData = d3.select(this).datum();
    d3.select(this).transition().duration(120)
        .attr("fill", d => getColor(d.group))
        .attr("stroke-width", 1)
        .attr("r", r => r.size / 5);
    zoomContainer.selectAll(".node-labels text")
        .each(function (d) {
            if (d.id === nodeData.id) {		// Check if Node ID is the same as Label ID
                d3.select(this).transition().duration(120)
                    .attr("visibility", "hidden");    // Show Label
            }
        })
})



// Adding Drag Behavior
node.call(d3.drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended));

// Setting position of each node (and link) for every simulation tick.
simulation.on("tick", () => {
    link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);
    node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
    nodeLabel
        .attr("x", d => d.x)
        .attr("y", d => d.y - (d.size / 5) * 1.5);

});


//  Simulating Force
// ==================
// Drag Start
function dragstarted(event) {
    node.attr("cursor", "grabbing")
    // if (!event.active) simulation.alphaTarget(0.5).restart();  // Comment Out for Render
    event.subject.fx = event.subject.x
    event.subject.fy = event.subject.y
}

// Dragging
function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
}

// Drag End
function dragended(event) {
    node.attr("cursor", "grab")
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
}

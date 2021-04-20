// Ingesting data from DOM:
const hour_freq = JSON.parse(document.getElementById('user_req_hourly').textContent);
const daily_freq = JSON.parse(document.getElementById('user_req_daily').textContent);

// Data trace for hourly request frequency:
const hourly_freq_trace = [{
    type: "scatter",
    name: "Hourly Requests",
    fill: 'tozeroy', 
    marker: {
        color: '#32CD32'
      },    
    x: hour_freq["Index"].map(date => Date.parse(date)),
    y: hour_freq["Data"],
}];

Plotly.newPlot("hourly_requests_graph", hourly_freq_trace, {
    title: "Hourly Requests",
    margin: {
        t: 40
    },
    plot_bgcolor: "rgba(0,0,0,0)",
    paper_bgcolor: "rgba(0,0,0,0)",
    
    font: {
        color: "#b2becd"
    }, 
    
    // Axis Title Formatting:
    xaxis: {
        title: "Local Time (UTC-4)",
        type: 'date',
        tickformat: '%m-%d-%H:%M',
        nticks: 6,
        gridcolor: "#b2becd",
        linecolor: "#b2becd",
        linewidth: 1,
        mirror: true, 
        showgrid: false
    },

    yaxis: {
        title: "HTTP Requests",
        gridcolor: "#b2becd",
        linecolor: "#b2becd",
        linewidth: 2,
        mirror: true,
        showgrid: false
    }
});

// Data trace for daily request frequency:
const daily_freq_trace = [{
    type: "scatter",
    name: "Daily Requests",
    fill: "tozeroy",
    x: daily_freq["Index"].map(date => Date.parse(date)),
    y: daily_freq["Data"]
}];

Plotly.newPlot("daily_requests_graph", daily_freq_trace, {
    title: "Daily Requests",
    margin: {
        t: 40
    },
    plot_bgcolor: "rgba(0,0,0,0)",
    paper_bgcolor: "rgba(0,0,0,0)",
    
    font: {
        color: "#b2becd"
    }, 
    
    // Axis Title Formatting:
    xaxis: {
        title: "Local Time (UTC-4)",
        type: 'date',
        tickformat: '%m-%d-%H:%M',
        nticks: 6,
        gridcolor: "#b2becd",
        linecolor: "#b2becd",
        linewidth: 1,
        mirror: true, 
        showgrid: false
    },

    yaxis: {
        title: "HTTP Requests",
        gridcolor: "#b2becd",
        linecolor: "#b2becd",
        linewidth: 2,
        mirror: true,
        showgrid: false
    }

});
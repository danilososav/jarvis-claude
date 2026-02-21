import React from 'react';
import Chart from 'react-apexcharts';
import './ApexChartCard.css';

/**
 * ApexChartCard - Componente para renderizar gráficos profesionales
 * Recibe configuración y datos del backend (Python)
 * Soporta: bar, pie, line, donut, horizontalBar, bubble, scatter, gauge
 */
export function ApexChartCard({ config, data }) {
  if (!config || !data || data.length === 0) {
    return null;
  }

  const { type, title, description } = config;

  // Preparar datos según tipo de gráfico
  const prepareChartData = () => {
    switch (type) {
      case 'bar':
        return prepareBarChart();
      case 'pie':
        return preparePieChart();
      case 'line':
        return prepareLineChart();
      case 'donut':
        return prepareDonutChart();
      case 'horizontalBar':
        return prepareHorizontalBarChart();
      case 'bubble':
        return prepareBubbleChart();
      case 'scatter':
        return prepareScatterChart();
      case 'gauge':
        return prepareGaugeChart();
      default:
        return prepareBarChart();
    }
  };

  // BAR CHART
  const prepareBarChart = () => {
    const categories = data.map(item => {
      const name = item.cliente || item.name || 'N/A';
      return name.length > 20 ? name.substring(0, 20) + '...' : name;
    });

    const values = data.map(item => {
      const facturacion = item.facturacion || 0;
      return Math.round(facturacion / 1000000);
    });

    const options = {
      chart: {
        type: 'bar',
        toolbar: {
          show: true,
          tools: {
            download: true,
            selection: false,
            zoom: false,
            zoomin: false,
            zoomout: false,
            pan: false,
            reset: false
          }
        },
        background: 'transparent',
        foreColor: '#e6edf3',
        fontFamily: 'Inter, system-ui, sans-serif',
        animations: {
          enabled: true,
          easing: 'easeinout',
          speed: 800,
          animateGradually: {
            enabled: true,
            delay: 150
          }
        }
      },
      plotOptions: {
        bar: {
          borderRadius: 8,
          columnWidth: '60%',
          dataLabels: {
            position: 'top'
          }
        }
      },
      colors: ['#58a6ff'],
      fill: {
        type: 'gradient',
        gradient: {
          shade: 'dark',
          type: 'vertical',
          shadeIntensity: 0.3,
          gradientToColors: ['#1f6feb'],
          inverseColors: false,
          opacityFrom: 1,
          opacityTo: 0.8,
          stops: [0, 100]
        }
      },
      dataLabels: {
        enabled: true,
        formatter: (val) => `${val.toLocaleString('es-PY')}M`,
        offsetY: -20,
        style: {
          fontSize: '11px',
          colors: ['#e6edf3'],
          fontWeight: 600
        }
      },
      xaxis: {
        categories: categories,
        labels: {
          style: {
            colors: '#8b949e',
            fontSize: '12px'
          },
          rotate: -45,
          rotateAlways: false
        },
        axisBorder: {
          show: true,
          color: '#30363d'
        },
        axisTicks: {
          show: true,
          color: '#30363d'
        }
      },
      yaxis: {
        title: {
          text: 'Millones Gs',
          style: {
            color: '#8b949e',
            fontSize: '12px',
            fontWeight: 500
          }
        },
        labels: {
          style: {
            colors: '#8b949e',
            fontSize: '12px'
          },
          formatter: (val) => `${val.toLocaleString('es-PY')}M`
        }
      },
      grid: {
        borderColor: '#30363d',
        strokeDashArray: 3,
        xaxis: {
          lines: {
            show: false
          }
        },
        yaxis: {
          lines: {
            show: true
          }
        }
      },
      tooltip: {
        theme: 'dark',
        style: {
          fontSize: '12px',
          fontFamily: 'Inter, system-ui, sans-serif'
        },
        y: {
          formatter: (val) => `${val.toLocaleString('es-PY')} Millones Gs`
        },
        marker: {
          show: true
        }
      }
    };

    const series = [
      {
        name: 'Facturación',
        data: values
      }
    ];

    return { options, series };
  };

  // PIE CHART
  const preparePieChart = () => {
    const labels = data.map(item => {
      const name = item.cliente || item.name || 'N/A';
      return name.length > 15 ? name.substring(0, 15) + '...' : name;
    });

    const values = data.map(item => 
      parseFloat((item.market_share || 0).toFixed(2))
    );

    const options = {
      chart: {
        type: 'pie',
        background: 'transparent',
        foreColor: '#e6edf3',
        fontFamily: 'Inter, system-ui, sans-serif',
        animations: {
          enabled: true,
          easing: 'easeinout',
          speed: 800,
          animateGradually: {
            enabled: true,
            delay: 150
          }
        }
      },
      labels: labels,
      colors: ['#58a6ff', '#79c0ff', '#1f6feb', '#0969da', '#388bfd', '#6e40aa', '#f85149'],
      fill: {
        type: 'gradient',
        gradient: {
          shade: 'dark',
          type: 'horizontal',
          shadeIntensity: 0.5,
          inverseColors: false,
          opacityFrom: 1,
          opacityTo: 0.8
        }
      },
      legend: {
        position: 'bottom',
        fontSize: '12px',
        labels: {
          colors: '#e6edf3'
        },
        markers: {
          width: 12,
          height: 12,
          radius: 3
        }
      },
      dataLabels: {
        enabled: true,
        style: {
          fontSize: '12px',
          fontWeight: 600,
          colors: ['#0d1117']
        },
        formatter: (val) => `${val.toFixed(1)}%`,
        dropShadow: {
          enabled: false
        }
      },
      tooltip: {
        theme: 'dark',
        style: {
          fontSize: '12px',
          fontFamily: 'Inter, system-ui, sans-serif'
        },
        y: {
          formatter: (val) => `${val.toFixed(2)}%`
        }
      },
      responsive: [
        {
          breakpoint: 480,
          options: {
            chart: {
              width: 300
            },
            legend: {
              position: 'bottom'
            }
          }
        }
      ]
    };

    return { options, series: values };
  };

  // LINE CHART
  const prepareLineChart = () => {
    const categories = data.map(item => {
      const name = item.cliente || item.name || item.periodo || 'N/A';
      return name.length > 15 ? name.substring(0, 15) + '...' : name;
    });

    const values = data.map(item => {
      const facturacion = item.facturacion || 0;
      return Math.round(facturacion / 1000000);
    });

    const options = {
      chart: {
        type: 'line',
        toolbar: {
          show: true,
          tools: {
            download: true,
            selection: false,
            zoom: true,
            zoomin: true,
            zoomout: true,
            pan: true,
            reset: true
          }
        },
        background: 'transparent',
        foreColor: '#e6edf3',
        fontFamily: 'Inter, system-ui, sans-serif',
        animations: {
          enabled: true,
          easing: 'easeinout',
          speed: 800,
          animateGradually: {
            enabled: true,
            delay: 150
          }
        }
      },
      colors: ['#58a6ff'],
      stroke: {
        curve: 'smooth',
        width: 3
      },
      markers: {
        size: 5,
        colors: ['#58a6ff'],
        strokeColors: '#0d1117',
        strokeWidth: 2,
        hover: {
          size: 7
        }
      },
      dataLabels: {
        enabled: false
      },
      xaxis: {
        categories: categories,
        labels: {
          style: {
            colors: '#8b949e',
            fontSize: '12px'
          },
          rotate: -45
        },
        axisBorder: {
          show: true,
          color: '#30363d'
        }
      },
      yaxis: {
        title: {
          text: 'Millones Gs',
          style: {
            color: '#8b949e',
            fontSize: '12px',
            fontWeight: 500
          }
        },
        labels: {
          style: {
            colors: '#8b949e',
            fontSize: '12px'
          },
          formatter: (val) => `${val.toLocaleString('es-PY')}M`
        }
      },
      grid: {
        borderColor: '#30363d',
        strokeDashArray: 3
      },
      tooltip: {
        theme: 'dark',
        style: {
          fontSize: '12px',
          fontFamily: 'Inter, system-ui, sans-serif'
        },
        y: {
          formatter: (val) => `${val.toLocaleString('es-PY')} Millones Gs`
        }
      },
      fill: {
        type: 'gradient',
        gradient: {
          shade: 'dark',
          type: 'vertical',
          shadeIntensity: 0.2,
          gradientToColors: ['#1f6feb'],
          opacityFrom: 0.7,
          opacityTo: 0.3
        }
      }
    };

    const series = [
      {
        name: 'Facturación',
        data: values
      }
    ];

    return { options, series };
  };

  // DONUT CHART (nuevo)
  const prepareDonutChart = () => {
    const pieData = preparePieChart();
    
    // Modificar options para convertir a donut
    pieData.options.chart.type = 'donut';
    pieData.options.plotOptions = {
      pie: {
        donut: {
          size: '65%',
          labels: {
            show: true,
            name: {
              show: true,
              fontSize: '14px',
              color: '#e6edf3'
            },
            value: {
              show: true,
              fontSize: '20px',
              fontWeight: 600,
              color: '#58a6ff',
              formatter: (val) => `${parseFloat(val).toFixed(1)}%`
            },
            total: {
              show: true,
              label: 'Total',
              fontSize: '14px',
              color: '#8b949e',
              formatter: () => {
                const total = pieData.series.reduce((a, b) => a + b, 0);
                return `${total.toFixed(1)}%`;
              }
            }
          }
        }
      }
    };

    return pieData;
  };

  // HORIZONTAL BAR CHART (nuevo)
  const prepareHorizontalBarChart = () => {
    const barData = prepareBarChart();
    
    // Modificar para horizontal
    barData.options.chart.type = 'bar';
    barData.options.plotOptions.bar = {
      borderRadius: 8,
      horizontal: true,
      barHeight: '70%',
      dataLabels: {
        position: 'top'
      }
    };
    
    // Intercambiar ejes
    barData.options.yaxis = {
      labels: {
        style: {
          colors: '#8b949e',
          fontSize: '12px'
        }
      }
    };
    
    barData.options.xaxis = {
      title: {
        text: 'Millones Gs',
        style: {
          color: '#8b949e',
          fontSize: '12px'
        }
      },
      labels: {
        style: {
          colors: '#8b949e',
          fontSize: '12px'
        },
        formatter: (val) => `${val.toLocaleString('es-PY')}M`
      }
    };

    return barData;
  };

  // BUBBLE CHART (nuevo) - Usando scatter para evitar bug de rebote
  const prepareBubbleChart = () => {
    // Convertir a formato scatter con tamaños variables
    const scatterData = data.map(item => {
      const facturacion = item.facturacion || 0;
      const marketShare = item.market_share || 0;
      
      return {
        x: Math.round(facturacion / 1000000),
        y: parseFloat(marketShare.toFixed(2))
      };
    });

    const options = {
      chart: {
        type: 'scatter',
        toolbar: {
          show: true
        },
        background: 'transparent',
        foreColor: '#e6edf3',
        fontFamily: 'Inter, system-ui, sans-serif',
        zoom: {
          enabled: true,
          type: 'xy'
        }
      },
      colors: ['#58a6ff'],
      markers: {
        size: data.map((item, idx) => {
          // Tamaño basado en facturación (8-20px)
          const fac = item.facturacion || 0;
          const maxFac = Math.max(...data.map(d => d.facturacion || 0));
          return 8 + ((fac / maxFac) * 12);
        }),
        strokeWidth: 2,
        strokeColors: '#1f6feb',
        hover: {
          size: undefined,  // NO cambiar tamaño en hover
          sizeOffset: 0     // Sin offset
        }
      },
      states: {
        hover: {
          filter: {
            type: 'none'  // SIN efectos en hover
          }
        },
        active: {
          allowMultipleDataPointsSelection: false,
          filter: {
            type: 'none'
          }
        }
      },
      fill: {
        type: 'solid',
        opacity: 0.85
      },
      dataLabels: {
        enabled: false
      },
      xaxis: {
        title: {
          text: 'Facturación (Millones Gs)',
          style: {
            color: '#8b949e'
          }
        },
        labels: {
          style: {
            colors: '#8b949e'
          },
          formatter: (val) => `${val.toLocaleString('es-PY')}M`
        }
      },
      yaxis: {
        title: {
          text: 'Market Share (%)',
          style: {
            color: '#8b949e'
          }
        },
        labels: {
          style: {
            colors: '#8b949e'
          },
          formatter: (val) => `${val.toFixed(1)}%`
        }
      },
      grid: {
        borderColor: '#30363d',
        strokeDashArray: 3
      },
      legend: {
        show: false
      },
      tooltip: {
        theme: 'dark',
        custom: function({ dataPointIndex }) {
          const item = data[dataPointIndex];
          const cliente = item?.cliente || 'Cliente';
          const fac = item?.facturacion || 0;
          const ms = item?.market_share || 0;
          return `<div style="padding: 10px; background: #161b22; border: 1px solid #30363d; border-radius: 6px;">
            <strong style="color: #e6edf3;">${cliente}</strong><br/>
            <span style="color: #8b949e;">Facturación:</span> <span style="color: #58a6ff;">${(fac / 1000000).toLocaleString('es-PY')}M Gs</span><br/>
            <span style="color: #8b949e;">Market Share:</span> <span style="color: #58a6ff;">${ms.toFixed(2)}%</span>
          </div>`;
        }
      }
    };

    return { options, series: [{ name: 'Clientes', data: scatterData }] };
  };

  // SCATTER CHART (nuevo)
  const prepareScatterChart = () => {
    const scatterSeries = [{
      name: 'Clientes',
      data: data.map(item => ({
        x: Math.round((item.facturacion || 0) / 1000000),
        y: parseFloat((item.market_share || 0).toFixed(2))
      }))
    }];

    const options = {
      chart: {
        type: 'scatter',
        toolbar: {
          show: true
        },
        background: 'transparent',
        foreColor: '#e6edf3',
        fontFamily: 'Inter, system-ui, sans-serif',
        zoom: {
          enabled: true,
          type: 'xy'
        }
      },
      colors: ['#58a6ff'],
      markers: {
        size: 8,
        strokeWidth: 2,
        strokeColors: '#0d1117',
        hover: {
          size: 10
        }
      },
      xaxis: {
        title: {
          text: 'Facturación (Millones Gs)',
          style: {
            color: '#8b949e'
          }
        },
        labels: {
          style: {
            colors: '#8b949e'
          },
          formatter: (val) => `${val.toLocaleString('es-PY')}M`
        }
      },
      yaxis: {
        title: {
          text: 'Market Share (%)',
          style: {
            color: '#8b949e'
          }
        },
        labels: {
          style: {
            colors: '#8b949e'
          },
          formatter: (val) => `${val.toFixed(1)}%`
        }
      },
      grid: {
        borderColor: '#30363d',
        strokeDashArray: 3
      },
      tooltip: {
        theme: 'dark',
        custom: function({ dataPointIndex, w }) {
          const point = w.config.series[0].data[dataPointIndex];
          const cliente = data[dataPointIndex]?.cliente || 'Cliente';
          return `<div style="padding: 10px; background: #161b22; border: 1px solid #30363d;">
            <strong style="color: #e6edf3;">${cliente}</strong><br/>
            Facturación: ${point.x.toLocaleString('es-PY')}M Gs<br/>
            Market Share: ${point.y.toFixed(2)}%
          </div>`;
        }
      }
    };

    return { options, series: scatterSeries };
  };

  // GAUGE CHART (nuevo)
  const prepareGaugeChart = () => {
    // Calcular valor para gauge (% del líder vs total)
    const total = data.reduce((sum, item) => sum + (item.facturacion || 0), 0);
    const leader = data[0] || {};
    const leaderValue = leader.facturacion || 0;
    const percentage = total > 0 ? (leaderValue / total * 100) : 0;

    const options = {
      chart: {
        type: 'radialBar',
        background: 'transparent',
        foreColor: '#e6edf3',
        fontFamily: 'Inter, system-ui, sans-serif'
      },
      plotOptions: {
        radialBar: {
          startAngle: -135,
          endAngle: 135,
          hollow: {
            margin: 0,
            size: '70%',
            background: 'transparent'
          },
          track: {
            background: '#30363d',
            strokeWidth: '100%',
            margin: 0
          },
          dataLabels: {
            show: true,
            name: {
              show: true,
              fontSize: '14px',
              color: '#8b949e',
              offsetY: -10
            },
            value: {
              show: true,
              fontSize: '30px',
              fontWeight: 700,
              color: '#58a6ff',
              offsetY: 5,
              formatter: (val) => `${val.toFixed(1)}%`
            }
          }
        }
      },
      fill: {
        type: 'gradient',
        gradient: {
          shade: 'dark',
          type: 'horizontal',
          shadeIntensity: 0.5,
          gradientToColors: ['#1f6feb'],
          inverseColors: false,
          opacityFrom: 1,
          opacityTo: 1,
          stops: [0, 100]
        }
      },
      stroke: {
        lineCap: 'round'
      },
      labels: [config.gauge_label || leader.cliente || 'Participación']
    };

    return { options, series: [percentage] };
  };

  const chartData = prepareChartData();

  return (
    <div className="apex-chart-card">
      <div className="chart-header">
        <h3 className="chart-title">{title}</h3>
        <p className="chart-description">{description}</p>
      </div>
      
      <div className="chart-body">
        <Chart
          options={chartData.options}
          series={chartData.series}
          type={type === 'horizontalBar' ? 'bar' : type === 'gauge' ? 'radialBar' : type === 'bubble' ? 'scatter' : type}
          height={450}
        />
      </div>
    </div>
  );
}
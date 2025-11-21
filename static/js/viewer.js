// static/js/viewer.js
document.addEventListener('DOMContentLoaded', () => {
  // Handle main page heatmaps
  const heatmapContainers = document.querySelectorAll('.heatmaps');
  heatmapContainers.forEach(container => {
    const checkboxes = container.parentElement.querySelectorAll('input[type="checkbox"]');
    const heatmaps = container.querySelectorAll('.heatmap');
    
    checkboxes.forEach(checkbox => {
      checkbox.addEventListener('change', function() {
        const channel = this.getAttribute('data-channel');
        const heatmap = container.querySelector(`.heatmap[data-channel="${channel}"]`);
        
        if (heatmap) {
          if (this.checked) {
            heatmap.style.display = 'flex';
          } else {
            heatmap.style.display = 'none';
          }
        }
      });
    });
  });

  // Handle detail page sliders
  document.querySelectorAll('.slider-block').forEach(block => {
    const week   = block.dataset.week;
    const folder = block.dataset.folder;           
    const viewer = block.querySelector('.viewer');
    const slider = block.querySelector('.z-slider');
    const controls = Array.from(block.querySelectorAll('.channel-cbx'));

    if (!viewer || !slider) return; // Skip if not a detail page

    // Create an <img> for each channel
    const chanImgs = {};
    controls.forEach(cbx => {
      const chan = cbx.dataset.chan;
      const img = document.createElement('img');
      img.className = 'chan-img';
      img.dataset.chan = chan;
      img.style.position = 'absolute';
      img.style.top  = '0';
      img.style.left = '0';
      img.style.width  = '100%';
      img.style.height = '100%';
      img.style.objectFit = 'contain';
      img.hidden = true;
      viewer.appendChild(img);
      chanImgs[chan] = img;

      // when you toggle a checkbox, update the displayed images
      cbx.addEventListener('change', () => {
        updateImages(slider.value);
      });
    });

    // Handler to swap in the right PNGs
    function updateImages(z) {
      controls.forEach(cbx => {
        const chan = cbx.dataset.chan;
        const img  = chanImgs[chan];
        if (cbx.checked) {
          let imagePath;
          
          if (week === 'overview') {
            // Handle overview data - different path pattern
            let sliderName = block.querySelector('h2').textContent.toLowerCase().replace(/ /g, '_');
            
            if (folder.includes('overview_processed_detailed')) {
              // Format: overview_processed_detailed/healthy_airway/overview_healthy_airway_z1_ch1.png
              imagePath = `/static/${folder}/overview_${sliderName}_z${z}_ch${chan}.png`;
            } else if (folder.includes('vessel_processed_detailed')) {
              // Format: vessel_processed_detailed/week3/fibrotic_arteriole/week3_fibrotic_arteriole_z1_ch1.png
              const weekMatch = folder.match(/week(\d+)/);
              const weekNum = weekMatch ? weekMatch[1] : '3';
              imagePath = `/static/${folder}/week${weekNum}_${sliderName}_z${z}_ch${chan}.png`;
            } else {
              // Fallback for other overview data
              imagePath = `/static/${folder}/${sliderName}_z${z}_ch${chan}.png`;
            }
          } else {
            // Regular week data - handle different naming patterns
            let sliderName = block.querySelector('h2').textContent.toLowerCase();
            
            if (folder.includes('processed_detailed/week3') && folder.includes('kmc')) {
              // Fibrotic alveoli format: week3_kmc2_z1_ch1.png
              const kmcMatch = folder.match(/kmc(\d+)/);
              const kmcNum = kmcMatch ? kmcMatch[1] : '2';
              imagePath = `/static/${folder}/week3_kmc${kmcNum}_z${z}_ch${chan}.png`;
            } else if (folder.includes('processed_detailed/week0')) {
              // Healthy alveoli format: week0_z1_ch1.png
              imagePath = `/static/${folder}/week0_z${z}_ch${chan}.png`;
            } else if (folder.includes('vessel_processed_detailed')) {
              // Vessel data format: week3_fibrotic_venule_z1_ch1.png
              const weekMatch = folder.match(/week(\d+)/);
              const weekNum = weekMatch ? weekMatch[1] : '3';
              // Extract tissue name from folder path
              const folderParts = folder.split('/');
              const tissueName = folderParts[folderParts.length - 1]; // Get last part of folder path
              imagePath = `/static/${folder}/week${weekNum}_${tissueName}_z${z}_ch${chan}.png`;
            } else {
              // Fallback to original logic
              sliderName = sliderName.replace(/^week\d*_?/, '');
              imagePath = `/static/${folder}/week${week}/${chan}/week${week}_${sliderName}_ch${chan}_z${z}.png`;
            }
          }
          
          // Debug: log the path being tried
          console.log('Loading image:', imagePath);
          console.log('Components:', { week, sliderName: block.querySelector('h2').textContent, chan, z, folder });
          
          img.src = imagePath;
          img.hidden = false;
          
          // Add error handling to catch failed image loads
          img.onerror = function() {
            console.error('Failed to load image:', imagePath);
            console.log('Image element:', this);
          };
          
          img.onload = function() {
            console.log('Successfully loaded image:', imagePath);
          };
        } else {
          img.hidden = true;
        }
      });
    }

    // Wire up the slider
    slider.addEventListener('input', () => {
      updateImages(slider.value);
    });

    // Initialize: check any default-checked checkboxes and load initial images
    controls.forEach(cbx => {
      if (cbx.checked) {
        updateImages(slider.value);
        return; // Only need to call once if any checkbox is checked
      }
    });
    // If no checkboxes are checked by default, check the first one
    if (!controls.some(cbx => cbx.checked) && controls.length > 0) {
      controls[0].checked = true;
      updateImages(slider.value);
    }
  });
});
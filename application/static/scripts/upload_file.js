let dropArea = document.getElementById('file-drop-box');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
      dropArea.addEventListener(eventName, preventDefaults, false)
    });
    
    function preventDefaults (e) {
      e.preventDefault()
      e.stopPropagation()
    };

    ['dragenter', 'dragover'].forEach(eventName => {
      dropArea.addEventListener(eventName, highlight, false)
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
      dropArea.addEventListener(eventName, unhighlight, false)
    });
    
    function highlight(e) {
      dropArea.classList.add('highlight')
    }
    
    function unhighlight(e) {
      dropArea.classList.remove('highlight')
    }

    dropArea.addEventListener('drop', handleDrop, false)

  function handleDrop(e) {
    let dt = e.dataTransfer
    let files = dt.files
    const file = [...files][0];
    setFileInput(file);
    handleFile(files)
}

// Called whenever a file is choosen in any way (drop or click)
function handleFile(files) {
    const file = [...files][0];
    const filename_tag = document.getElementById('uploaded-file-name');
    const filename = document.getElementById('fileElem').files[0].name;
    filename_tag.innerText = filename;
    setPageRange(file);
}

function setFileInput(file) {
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    fileElem = document.getElementById('fileElem');
    fileElem.files = dataTransfer.files;
}

function setPageRange(file) {
  const formData = new FormData();
  formData.append('file', file);
  fetch('/generate_deck/number_of_pdf_pages', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    const page_range = data['page_range'];
    // Make choose pages active
    const n_pages_box = document.getElementById('n-pages-box');
    n_pages_box.classList.add('n-pages-box-active')
    // Set allowed page range
    const start_page = document.getElementById('start-page');
    const end_page = document.getElementById('end-page');
    start_page.min = page_range[0];
    start_page.max = page_range[1];
    end_page.min = page_range[0];
    end_page.max = page_range[1];
    end_page.value = page_range[1];
    console.log(data);
  })
  .catch(error => {
    // Other file type. Remove PDF specific stuff set above
    const n_pages_box = document.getElementById('n-pages-box');
    n_pages_box.classList.remove('n-pages-box-active')
  });
}
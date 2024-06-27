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

function handleFile(files) {
    const file = [...files][0];
    const filename_tag = document.getElementById('uploaded-file-name');
    const filename = document.getElementById('fileElem').files[0].name;
    filename_tag.innerText = filename;
}

function setFileInput(file) {
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    fileElem = document.getElementById('fileElem');
    fileElem.files = dataTransfer.files;
}
const field_row_container = document.getElementById('container')
let FIELD_ID_COUNT = 1



function addFieldRow(){
  const div = document.createElement('div');
  FIELD_ID_COUNT = FIELD_ID_COUNT + 1;

  div.classList.add('row');
  div.innerHTML =
  `
        <div class="row push-down-containers" id="row-1">
            <div class="col-sm">
                <label for="field-name-${FIELD_ID_COUNT}"><h5>Field name</h5></label>
                <input class="form-control form-control-lg " type="text" id="field-name-${FIELD_ID_COUNT}" name="field-name-${FIELD_ID_COUNT}" required>
                <div class="form-text">
                    Use '_' symbol to separate multiple-word names
                </div>
            </div>
            <div class="col-sm">
                <label for="field-type-${FIELD_ID_COUNT}"><h5>Field type</h5></label>
                <select class="form-control form-control-lg" id="field-type-${FIELD_ID_COUNT}" name="field-type-${FIELD_ID_COUNT}" required>
                    <option>Long Text</option>
                    <option>Text</option>
                    <option>Float</option>
                    <option>Integer</option>
                    <option>Boolean</option>
                    <option>Date</option>
                    Check for table or columns name conventions </select>
            </div>
            <div class="col-sm remove-button">
                <button type="button" class="btn btn-secondary btn-sm" onclick="removeFieldRow(event)"
                        id="row-remove-button-1" style="">Remove
                </button>
            </div>
        </div>
    `;
    div.id = 'row-' + FIELD_ID_COUNT;
    field_row_container.appendChild(div);
}



function removeFieldRow(e){
  e.preventDefault();
  let element = e.target;
  const id = element.id.split('-').pop();
  console.log(id);
  document.getElementById(`row-${id}`).remove();
}


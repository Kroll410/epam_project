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
                    Note: date type should be type in format 'MM-DD-YYYY'
                    <br>
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


const data_row_container = document.getElementById('new-data-row')
let ROW_ID_COUNT = 1

function addDataRow(){
  const tr = document.createElement('tr');
  ROW_ID_COUNT = ROW_ID_COUNT + 1;

  tr.classList.add('row');
  tr.innerHTML =
  `
   <tr id="data-row-${ROW_ID_COUNT}">
        <form method="POST">
            {% for idx in range(data['amount_of_fields']) %}
            {% if idx == 0 or idx == data['amount_of_fields'] - 1 %}
            <th scope="col"></th>
            {% else %}
            <th scope="col">
                <input class="form-control form-control-sm add-new-row" type="text">
            </th>
            {% endif %}
            {% endfor %}
        </form>
    </tr>
    `;
    data_row_container.appendChild(tr);
    console.log('kek')
}
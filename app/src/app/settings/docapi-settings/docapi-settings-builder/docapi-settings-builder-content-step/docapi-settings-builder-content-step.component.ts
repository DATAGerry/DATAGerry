/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 NETHINKS GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, OnInit, Input } from '@angular/core';
import { CmdbMode } from '../../../../framework/modes.enum';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';


declare var tinymce;

@Component({
  selector: 'cmdb-docapi-settings-builder-content-step',
  templateUrl: './docapi-settings-builder-content-step.component.html',
  styleUrls: ['./docapi-settings-builder-content-step.component.scss']
})
export class DocapiSettingsBuilderContentStepComponent implements OnInit {

  @Input() public mode: CmdbMode;
  public modes = CmdbMode;
  public contentForm: FormGroup;

  public editorConfig = {
    base_url: '/assets/tinymce',
    suffix: '.min',
    height: 500,
    menubar: false,
    plugins: [
      'advlist autolink lists link image charmap print preview anchor',
      'searchreplace visualblocks code fullscreen',
      'insertdatetime media table paste code help wordcount'
    ],
    toolbar:
      'undo redo | formatselect | bold italic backcolor | \
      alignleft aligncenter alignright alignjustify | \
      bullist numlist outdent indent | image | removeformat | help',
    paste_data_images: true,
    automatic_uploads: true,
    file_picker_types: 'image',
    file_picker_callback: function (cb, value, meta) {
      let input = document.createElement('input');
      input.setAttribute('type', 'file');
      input.setAttribute('accept', 'image/*');
      input.onchange = function () {
        let file = input.files[0];
        let reader = new FileReader();
        reader.onload = function () {
          let id = 'blobid' + (new Date()).getTime();
          let blobCache = tinymce.activeEditor.editorUpload.blobCache;
          let base64 = (<string>reader.result).split(',')[1];
          let blobInfo = blobCache.create(id, file, base64);
          blobCache.add(blobInfo);
          cb(blobInfo.blobUri(), { title: file.name });
        };
        reader.readAsDataURL(file);
      };
      input.click();
    }
  }

  constructor() { 
    this.contentForm = new FormGroup({
      content: new FormControl('', Validators.required)
    });
  }

  public get content() {
    return this.contentForm.get('content');
  }

  ngOnInit() {
  }

}

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
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { CmdbMode } from '../../../../framework/modes.enum';
import { TemplateHelperService } from '../../../services/template-helper.service';


declare var tinymce;

@Component({
  selector: 'cmdb-docapi-settings-builder-content-step',
  templateUrl: './docapi-settings-builder-content-step.component.html',
  styleUrls: ['./docapi-settings-builder-content-step.component.scss']
})
export class DocapiSettingsBuilderContentStepComponent implements OnInit {

  @Input()
  set preData(data: any) {
    if (data !== undefined) {
      this.contentForm.patchValue(data);
    }
  }

  @Input()
  set typeParam(data: any) {
    if(data) {
      if(data.type) {
        this.templateHelperData = this.templateHelperService.getObjectTemplateHelperData(data.type);
      }
    }
  }

  @Input() public mode: CmdbMode;
  public modes = CmdbMode;
  public contentForm: FormGroup;
  public templateHelperData: any;

  public editorConfig = {
    base_url: '/assets/tinymce',
    suffix: '.min',
    height: 500,
    menubar: true,
    plugins: [
      'advlist autolink lists link image charmap print preview anchor',
      'searchreplace visualblocks code fullscreen',
      'insertdatetime media table paste code help wordcount',
      'noneditable, pagebreak'
    ],
    toolbar:
      'undo redo | formatselect | bold italic backcolor | \
      alignleft aligncenter alignright alignjustify | \
      bullist numlist outdent indent | image | removeformat | pagebreak | help | cmdbdata | barcode',
    noneditable_noneditable_class: 'mceNonEditable',
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
    },
    pagebreak_separator: '<pdf:nextpage />',
    extended_valid_elements: 'pdf:barcode[*]',
    custom_elements: 'pdf:barcode',
    valid_children: '-pdf:barcode[*]',
    content_css: '/assets/css/tinymce_custom.css',
    setup: (editor) => {
      editor.ui.registry.addMenuButton('cmdbdata', {
        text: 'CMDB Data',
        fetch: (callback) => {
          let items = this.getCmdbDataMenuItems(editor);
          callback(items);
        }
      });
      editor.ui.registry.addMenuButton('barcode', {
        text: 'Barcode',
        fetch: (callback) => {
          let items = this.getBarcodeMenuItems(editor);
          callback(items);
        }
      });
    }
  }

  constructor(private templateHelperService: TemplateHelperService) { 
    this.contentForm = new FormGroup({
      template_data: new FormControl('', [Validators.required, Validators.max(15*1024*1024)])
    });
  }

  public get content() {
    return this.contentForm.get('template_data');
  }

  public getCmdbDataMenuItems(editor, templateHelperData = this.templateHelperData) {
    let items = [];
    for(const item of templateHelperData) {
      if(item.subdata) {
        items.push({
          type: 'nestedmenuitem',
          text: item.label,
          getSubmenuItems: () => {
            return this.getCmdbDataMenuItems(editor, item.subdata);
          }
        });
      }
      else {
        items.push({
          type: 'menuitem',
          text: item.label,
          onAction: function () {
            editor.insertContent(item.templatedata);
          }
        });
      }
    }
    return items;
  }


  public getBarcodeMenuItems(editor) {
    let items = [];
    items.push({
      type: 'menuitem',
      text: 'QR Code',
      onAction: function() {
        let selection = editor.selection.getNode();
        let preData = {};
        if(selection.tagName === 'PDF:BARCODE') {
          preData['type'] = selection.attributes.getNamedItem('type').value;
          preData['content'] = selection.attributes.getNamedItem('value').value;
        }
        editor.windowManager.open({
          title: 'Insert Barcode',
          body: {
            type: 'panel',
            items: [
              {
                type: 'input',
                name: 'content',
                label: 'Barcode Content'
              },
              {
                type: 'selectbox',
                name: 'type',
                label: 'Barcode Type',
                items: [
                  { value: 'qr', text: 'QR' },
                  { value: 'code128', text: 'Code 128' },
                ]
              }
            ]
          },
          buttons: [
            {
              type: 'submit',
              text: 'OK'
            }
          ],
          initialData: preData,
          onSubmit: function(dialogApi) {
            let barcodeContent = dialogApi.getData()['content'];
            let barcodeType = dialogApi.getData()['type'];
            let barcodeElementAttr = {
              class: 'mceNonEditable',
              type: barcodeType,
              value: barcodeContent
            };
            if(barcodeType === 'qr') {
              barcodeElementAttr['barwidth'] = '3cm';
              barcodeElementAttr['barheight'] = '3cm';
            }
            let barcodeElement = editor.dom.create('pdf:barcode', barcodeElementAttr);
            //edit barcode: remove existing and set cur
            if(preData['content']) {
              let selectionNext = editor.selection.getNode().nextSibling;
              editor.dom.remove(selection);
              if(selectionNext) {
                editor.selection.setCursorLocation(selectionNext);
              }
            }
            //insert new barcode
            editor.insertContent(barcodeElement.outerHTML);
            dialogApi.close();
          }
        });
      }
    });
    return items;
  }

  ngOnInit() { }

}

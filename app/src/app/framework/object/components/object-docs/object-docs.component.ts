/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2024 becon GmbH
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

import { Component, OnChanges, Input, SimpleChanges } from '@angular/core';

import { RenderResult } from '../../../models/cmdb-render';
import { DocTemplate } from '../../../../docapi/models/cmdb-doctemplate';
import { DocapiService } from '../../../../docapi/docapi.service';
import { FileSaverService } from 'ngx-filesaver';
import { MatDialog } from '@angular/material/dialog';


@Component({
  selector: 'cmdb-object-docs',
  templateUrl: './object-docs.component.html',
  styleUrls: ['./object-docs.component.scss']
})
export class ObjectDocsComponent implements OnChanges {

  @Input() renderResult: RenderResult;
  docs: DocTemplate[];

  constructor(private docapiService: DocapiService, private fileSaverService: FileSaverService, private dialog: MatDialog) { }

  ngOnChanges(changes: SimpleChanges) {
    if (changes.renderResult && this.renderResult) {
      this.docapiService.getObjectDocTemplateList(this.renderResult.type_information.type_id)
        .subscribe((docs: DocTemplate[]) => {
          this.docs = docs;
        });
    }
  }

  public downloadDocument(templateId: number, objectId: number, docName: string) {
    const filename = docName + '.pdf';
    this.docapiService.getRenderedObjectDoc(templateId, objectId)
      .subscribe(res => this.saveFile(res, filename));
  }

  public saveFile(data: any, filename: string) {
    this.fileSaverService.save(data.body, filename);
  }

  openDocumentDialog(): void {
    const dialogRef = this.dialog.open(ObjectDocsComponent, {
      width: '400px',
      data: { docs: this.docs }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }

}

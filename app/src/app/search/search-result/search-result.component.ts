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

import { Component, ComponentRef, Input, OnDestroy, OnInit } from '@angular/core';
import { SearchResult } from '../models/search-result';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';
import { SearchResultPreviewComponent } from './search-result-preview.component';

@Component({
  selector: 'cmdb-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.scss']
})
export class SearchResultComponent implements OnInit, OnDestroy {

  @Input() searchResult: SearchResult = undefined;
  private modalRef: NgbModalRef;

  public constructor(private modalService: NgbModal) {
  }

  public ngOnInit(): void {
  }

  public ngOnDestroy(): void {
    if (this.modalRef) {
      this.modalRef.close();
    }
  }

  public openPreview() {
    this.modalRef = this.modalService.open(SearchResultPreviewComponent, { size: 'lg' });
    this.modalRef.componentInstance.renderResult = this.searchResult.result;
  }

}

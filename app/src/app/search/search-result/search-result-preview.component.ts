import { Component, Input, OnInit } from '@angular/core';
import { RenderResult } from '../../framework/models/cmdb-render';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { FormGroup } from '@angular/forms';
import { CmdbMode } from '../../framework/modes.enum';

@Component({
  templateUrl: './search-result-preview.component.html',
  styleUrls: ['./search-result-preview.component.scss']
})
export class SearchResultPreviewComponent implements OnInit {

  @Input() renderResult: RenderResult;
  public mode = CmdbMode.View;
  public formGroupDummy: FormGroup;

  constructor(public activeModal: NgbActiveModal) {
    this.formGroupDummy = new FormGroup({});
  }

  public ngOnInit(): void {
  }

}

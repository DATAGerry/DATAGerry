import { Component, OnInit } from '@angular/core';
import { FormioForm, FormioOptions } from 'angular-formio';

@Component({
  selector: 'cmdb-type-fields-step',
  templateUrl: './type-fields-step.component.html',
  styleUrls: ['./type-fields-step.component.scss']
})
export class TypeFieldsStepComponent implements OnInit {
  public form: FormioForm = {};
  public options: FormioOptions = {};

  constructor() {
    this.form.title = 'Cmdb Type Builder';
    this.form.components = [];
  }

  ngOnInit() {
  }

}

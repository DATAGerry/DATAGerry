import { Component, OnInit } from '@angular/core';
import { TypeService } from '../../../../services/type.service';

@Component({
  selector: 'cmdb-ref-field-edit',
  templateUrl: './ref-field-edit.component.html',
  styleUrls: ['./ref-field-edit.component.scss']
})
export class RefFieldEditComponent implements OnInit {

  private typeList;

  constructor(private typeService: TypeService) {
  }

  ngOnInit() {
    this.typeList = this.typeService.getTypeList();
  }

}

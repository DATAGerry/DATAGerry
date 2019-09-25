import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { TypeService } from '../../../framework/services/type.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { CmdbType } from '../../../framework/models/cmdb-type';

@Component({
  selector: 'cmdb-select-type',
  templateUrl: './select-type.component.html',
  styleUrls: ['./select-type.component.scss']
})
export class SelectTypeComponent implements OnInit {

  public typeForm: FormGroup;
  public typeList: CmdbType[];
  @Output() public typeChange: EventEmitter<CmdbType>;

  constructor(private typeService: TypeService) {
    this.typeChange = new EventEmitter<CmdbType>();
    this.typeForm = new FormGroup({
      typeID: new FormControl(null, Validators.required)
    });
  }

  public ngOnInit(): void {
    this.typeService.getTypeList().subscribe((typeList: CmdbType[]) => {
      this.typeList = typeList;
    });

    this.typeForm.get('typeID').valueChanges.subscribe((typeID: number) => {
      this.typeChange.emit(this.typeList.find(typeInstance => typeInstance.public_id === typeID));
    });
  }


}

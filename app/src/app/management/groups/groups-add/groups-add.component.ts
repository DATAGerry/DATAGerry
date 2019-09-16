import { Component, OnInit } from '@angular/core';
import { GroupService } from '../../services/group.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { RightService } from '../../services/right.service';
import { Right } from '../../models/right';
import { ToastService } from '../../../layout/services/toast.service';
import { Router } from '@angular/router';

@Component({
  selector: 'cmdb-groups-add',
  templateUrl: './groups-add.component.html',
  styleUrls: ['./groups-add.component.scss']
})
export class GroupsAddComponent implements OnInit {

  public addForm: FormGroup;
  public rightList: Right[];

  public constructor(private groupService: GroupService, private rightService: RightService,
                     private toastService: ToastService, private router: Router) {
    this.rightService.getRightList().subscribe((rightList: Right[]) => {
      this.rightList = rightList;
    });
  }

  public ngOnInit(): void {
    this.addForm = new FormGroup({
      name: new FormControl('', Validators.required),
      label: new FormControl(''),
      rights: new FormControl([])
    });
  }

  public get name() {
    return this.addForm.get('name');
  }

  public get label() {
    return this.addForm.get('label');
  }

  public get rights() {
    return this.addForm.get('rights');
  }

  public saveGroup() {
    const rawData = this.addForm.getRawValue();
    if (this.addForm.valid) {
      this.groupService.postGroup(rawData).subscribe(insertAck => {
          this.toastService.show(`Group was added with ID: ${insertAck}`);
        },
        (error) => {
          console.error(error);
        }, () => {
          this.router.navigate(['/management/groups/']);
        });
    }

  }

}

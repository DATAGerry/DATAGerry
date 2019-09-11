import { Component, OnDestroy, OnInit } from '@angular/core';
import { ObjectService } from '../../../services/object.service';
import { RenderResult } from '../../../models/cmdb-render';
import { AuthService } from '../../../../auth/services/auth.service';
import { User } from '../../../../management/models/user';
import { Subject } from 'rxjs';

@Component({
  selector: 'cmdb-your-items',
  templateUrl: './your-objects.component.html',
  styleUrls: ['./your-objects.component.scss']
})
export class YourObjectsComponent implements OnInit, OnDestroy {

  public userObjects: RenderResult[] = [];
  public userObjectsLength: number = 0;
  public currentUser: User;
  public dtOptions: DataTables.Settings = {};
  public dtTrigger: Subject<any> = new Subject();

  public constructor(private objectService: ObjectService, private authService: AuthService) {
    this.currentUser = this.authService.currentUserValue;
  }

  public ngOnInit(): void {
    this.dtOptions = {
      ordering: true,
      order: [[3, 'desc']],
      language: {
        search: '',
        searchPlaceholder: 'Filter...'
      }
    };
    this.objectService.getObjectsByUser(this.currentUser.public_id).subscribe((objectList: RenderResult[]) => {
        this.userObjects = objectList;
        this.userObjectsLength = this.userObjects.length;
      },
      (error) => {
        console.error(error);
        this.userObjectsLength = 0;
        this.dtTrigger.next();
      },
      () => {
        this.dtTrigger.next();
      });
  }

  public ngOnDestroy(): void {
    this.dtTrigger.unsubscribe();
  }

}

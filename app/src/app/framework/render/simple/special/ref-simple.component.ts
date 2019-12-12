import { Component, OnInit } from '@angular/core';
import { RenderField } from '../../fields/components.fields';
import { RenderResult } from '../../../models/cmdb-render';
import { ObjectService } from '../../../services/object.service';
import { HttpBackend, HttpClient } from '@angular/common/http';
import { HttpInterceptorHandler } from '../../../../services/api-call.service';
import { BasicAuthInterceptor } from '../../../../auth/interceptors/basic-auth.interceptor';
import { AuthService } from '../../../../auth/services/auth.service';

@Component({
  selector: 'cmdb-ref-simple',
  templateUrl: './ref-simple.component.html',
  styleUrls: ['./ref-simple.component.scss']
})
export class RefSimpleComponent extends RenderField implements OnInit {
  public refObject: RenderResult;

  constructor(private objectService: ObjectService, private backend: HttpBackend, private authService: AuthService) {
    super();
  }

  public ngOnInit(): void {
    const specialClient = new HttpClient(new HttpInterceptorHandler(this.backend, new BasicAuthInterceptor(this.authService)));
    if (this.data.value !== '' && this.data.value !== undefined && this.data.value !== null) {
      this.objectService.getObject(this.data.value, false, specialClient).subscribe((refObject: RenderResult) => {
        this.refObject = refObject;
      });
    }
  }
}

import { Router } from "@angular/router"
import {InitializeService} from "./initialize.service"
import { TestBed } from "@angular/core/testing"
import { RouterTestingModule } from "@angular/router/testing"
import { routes } from 'src/app/app-routing.module'
import { Observable } from "rxjs"
import { PaperlessUiSettings } from "../data/paperless-uisettings"
import { HttpClientTestingModule } from "@angular/common/http/testing"

fdescribe('InitializeService', () => {
    let router: Router;
    let initializeService: InitializeService;

    beforeEach(() =>
    {
        TestBed.configureTestingModule({
            providers: [InitializeService],
            imports: [
              RouterTestingModule.withRoutes(routes),
              HttpClientTestingModule
            ],
            teardown: { destroyAfterEach: true }
        });
        router = TestBed.inject(Router);
        initializeService = TestBed.inject(InitializeService);
    })

    fit('should return an object of type paperlessUiSettings when online', () =>
    {
        jest.spyOn(navigator, "onLine", "get").mockReturnValueOnce(true);
        const result = initializeService.initialize();
        expect(result).toBeInstanceOf(Observable<PaperlessUiSettings>);
    })

    fit('should navigate to offline route when offline', () =>
    {
        jest.spyOn(navigator, "onLine", "get").mockReturnValueOnce(false);
        const routerSpy = jest.spyOn(router, 'navigate');
        initializeService.initialize();
        expect(routerSpy).toHaveBeenCalledWith(['offline']);
    })

})
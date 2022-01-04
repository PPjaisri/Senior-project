import {
  RouteObject,
  useRoutes,
  useNavigate,
  useLocation
} from 'react-router-dom';
import {
  Button,
  Container
} from 'react-bootstrap';
import { Starter, SearchBar, BarLoader, ReturnResult } from './Component'
import './App.css';
import { useEffect, useState } from 'react'

function App() {

  let routes: RouteObject[] = [
    {
      path: "/",
      element: <Search />
    },
    {
      path: "/result",
      element: <Result />
    },
    {
      path: "/load",
      element: <BarLoader />
    }
  ];

  let element = useRoutes(routes);

  return (
    <div>
      {element}
    </div>
  );
}

function Search() {
  return (
    <Container>
      <Starter />
      <hr />
      <SearchBar />
    </Container>
  );
}

function Result() {
  let navigate = useNavigate();
  const { state }: any = useLocation();
  const res = state.result;

  function RenderResult() {
    if (res.length > 0) {
      return res.map((obj: any) => {
        return (
          <ReturnResult obj={ obj }/>
        );
      });
    } else {
      return (
        <div>
          <hr />
          <div className='jumbotron text-center'>
            <p>
              ไม่พบข่าวที่ต้องการค้นหา
            </p>
          </div>
        </div>
      );
    }
  }

  return (
    <div>
      <Container>
        <Starter />
        <RenderResult />
        <br />
        <br />
      </Container>
      <Button
        variant='success'
        className='full'
        onClick={() => navigate('/')}
      >
        Back
      </Button>
    </div>
  )
}

export default App;

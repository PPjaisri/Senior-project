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
import {
  Starter,
  SearchBar,
  Loader,
  ReturnResult
} from './Component'
import './App.css';

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
      element: <Loader />
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
  console.log(state);

  function RenderResult() {
    if (res) {
      if (res.length > 0) {
        return res.map((obj: any) => {
          return (
            <ReturnResult obj={obj} />
          );
        });
      } else {
        if (state.type === 'image') {
          return (
            <div>
              <hr />
              <div className='jumbotron text-center'>
                <p>{state.search}</p>
              </div>
            </div>
          );
        } else {
          return (
            <div>
              <hr />
              <div className='jumbotron text-center'>
                <p>ไม่พบข่าวที่ค้นหา</p>
              </div>
            </div>
          );
        }
      }
    } else {
      return (
        <div>
          <hr />
          <div className='jumbotron text-center'>
            <p>{ state.search }</p>
          </div>
        </div>
      );
    }
  }

  return (
    <div>
      <Starter />
      <RenderResult />
      <br />
      <br />
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

import React from 'react';

import Overview from "../pages/Overview.jsx";
import CryptoOverview from "../pages/analysis/CryptoOverview.jsx";
import URLOverview from "../pages/analysis/URLOverview.jsx";
import SourceViewer from "../pages/source/SourceViewer.jsx";
import ManifestOverview from "../pages/manifest/ManifestOverview.jsx";
import LogcatViewer from "../pages/device/LogcatViewer.jsx";
import { AreaChartOutlined, SearchOutlined, CodeOutlined } from '@ant-design/icons';

var routes = [
    {
      path: "/overview",
      visible: true,
      icon: <AreaChartOutlined />,
      name: "Overview",
      component: Overview
    },
    {
      path: "/source/show/:fileKey",
      visible: false,
      icon: <CodeOutlined />,
      name: "Source",
      component: SourceViewer,
    },
    {
      path: "/source",
      visible: true,
      icon: <CodeOutlined />,
      name: "Source",
      component: SourceViewer,
    },
    {
        path: "/analysis",
        visible: true,
        icon: <SearchOutlined />,
        name: "Static Analysis",
        sub: [
          {
            path: "/analysis/manifest",
            visible: true,
            name: "Manifest",
            component: ManifestOverview,
          },
          {
            path: "/analysis/crypto",
            visible: true,
            name: "Cryptography",
            component: CryptoOverview,
          },
          {
            path: "/analysis/urls",
            visible: true,
            name: "URLs",
            component: URLOverview,
          },
        ]
    },
    {
      path: "/device",
      visible: true,
      icon: <SearchOutlined />,
      name: "Device",
      sub: [
        {
          path: "/device/logcat",
          visible: true,
          name: "LogCat",
          component: LogcatViewer,
        }
      ]
  },

    { redirect: true, path: "/", pathTo: "/overview", name: "Overview" }
  ];

export default routes;

import Layout from '@/views/Layout'

// 通过服务端传回来的权限菜单列表，添加部分字段
export function makeRouter(routers) { // 遍历后台传来的路由字符串，转换为组件对象
	console.log(routers)
	let asyncRouter = routers.filter(route => {
		console.log('name:'+route.name +' path:'+route.path)
		//如果父节点有component字段
		if (route.component === 'Layout') {
			route.component = Layout
			// console.log('layout')
		} else {
			route.component = loadView(route.component)
		}

		if (route.children && route.children.length) {
			route.children = makeRouter(route.children);
		}
		return true
	});
	console.log('asyncrouter is:' + asyncRouter);
	return asyncRouter;
}

export const loadView = (view) => { // 路由懒加载
	return () => import(`@/views/${view}`);
}
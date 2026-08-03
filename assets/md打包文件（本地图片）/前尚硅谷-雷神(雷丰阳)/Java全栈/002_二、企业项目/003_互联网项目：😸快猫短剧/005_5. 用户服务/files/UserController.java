package com.lfy.kcat.user.controller;

import cn.dev33.satoken.session.SaSession;
import cn.dev33.satoken.stp.SaTokenInfo;
import cn.dev33.satoken.stp.StpUtil;
import cn.dev33.satoken.stp.parameter.SaLoginParameter;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author leifengyang
 * @version 1.0
 * @date 2025/9/13 14:21
 * @description:
 */
@RequestMapping("/user")
@RestController
public class UserController {

    @GetMapping("/doLogin")
    public String doLogin(String username, String password) {
        if ("admin".equals(username) && "123456".equals(password)) {
            //以前登录成功。去数据库查到这个用户id: 10001
            //代表10001号登录成功
            SaLoginParameter parameter = new SaLoginParameter();
            //扩展信息可以是从数据库查询到的用户基本信息
            parameter.setExtra("username","admin");
            parameter.setExtra("age","12");
            StpUtil.login(10001,parameter);
            return "登录成功";
        }

        //这个用户的会话是在redis中的额
        SaSession session = StpUtil.getSession();
        session.set("aaa","bbbb");
        return "登录失败";
    }

    @GetMapping("/isLogin")
    public String isLogin(){
        //自动知道当前是谁在登录和退出
        boolean login = StpUtil.isLogin();
        return "用户登录状态："+login;
    }

    @GetMapping("/logout")
    public String logout(){
        StpUtil.logout();
        return "用户已退出";
    }

    @GetMapping("/getCurrentUser")
    public String getCurrentUser(){

        Object loginId = StpUtil.getLoginId();
        return "登录用户的id是："+loginId;
    }


    /**
     * 只有在集成 sa-token-jwt 插件后才可以使用 extra 扩展参数
     * 用户将来的扩展信息，保存不到session中，但是可以和jwt
     * @return
     */

    @GetMapping("/getInfo")
    public String getInfo(){
        Object username = StpUtil.getExtra("username");
        Object age = StpUtil.getExtra("age");
        return "当前用户其他信息：用户名："+username+ "； 年龄："+age;
    }


    @GetMapping("/getToken")
    public String getToken(){
        String tokenName = StpUtil.getTokenName();
        String tokenValue = StpUtil.getTokenValue();
        SaTokenInfo tokenInfo = StpUtil.getTokenInfo();
        return "当前用户的token信息：name="+tokenName+"; value="+tokenValue;
    }
}
